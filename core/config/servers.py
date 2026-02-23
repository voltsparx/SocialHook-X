"""
SocialHook-X - Server Configuration Module

Manages server settings, ports, and host configurations.
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class ServerConfig:
    """Server configuration manager"""
    
    # Default values
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 8000
    DEFAULT_PORT_RANGE = (8000, 9000)
    
    # PHP Server
    PHP_HOST = "127.0.0.1"
    PHP_PORT = 8080
    
    # Flask Server
    FLASK_HOST = "127.0.0.1"
    FLASK_PORT = 8081
    
    # Server settings
    TIMEOUT = 30
    MAX_CONNECTIONS = 100
    DEBUG = False
    
    @classmethod
    def validate_port(cls, port: int) -> bool:
        """Validate port number
        
        Args:
            port: Port number
        
        Returns:
            True if valid port, False otherwise
        """
        return 1024 <= port <= 65535
    
    @classmethod
    def is_port_available(cls, port: int) -> bool:
        """Check if port is available
        
        Args:
            port: Port number
        
        Returns:
            True if port available, False otherwise
        """
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(('127.0.0.1', port))
            available = result != 0
            sock.close()
            return available
        except Exception as e:
            logger.error(f"Error checking port availability: {e}")
            return False
    
    @classmethod
    def get_available_port(cls, start_port: int = 8000) -> Optional[int]:
        """Get first available port starting from start_port
        
        Args:
            start_port: Starting port number
        
        Returns:
            Available port or None
        """
        for port in range(start_port, start_port + 100):
            if cls.is_port_available(port):
                return port
        return None
    
    @classmethod
    def get_server_config(cls) -> Dict:
        """Get server configuration
        
        Returns:
            Server configuration dictionary
        """
        return {
            "host": cls.PHP_HOST,
            "php_port": cls.PHP_PORT,
            "flask_port": cls.FLASK_PORT,
            "timeout": cls.TIMEOUT,
            "max_connections": cls.MAX_CONNECTIONS,
            "debug": cls.DEBUG
        }
    
    @classmethod
    def get_flask_config(cls) -> Dict:
        """Get Flask configuration
        
        Returns:
            Flask configuration dictionary
        """
        return {
            "host": cls.FLASK_HOST,
            "port": cls.FLASK_PORT,
            "debug": cls.DEBUG,
            "threaded": True
        }
