"""
SocialHook-X - Validators Utility Module

Provides input validation and sanitization functions.
"""

import logging
import re
from typing import Any, Optional

logger = logging.getLogger(__name__)


class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address
        
        Args:
            email: Email address
        
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_ip(ip: str) -> bool:
        """Validate IP address
        
        Args:
            ip: IP address
        
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, ip):
            return False
        
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL
        
        Args:
            url: URL
        
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return re.match(pattern, url, re.IGNORECASE) is not None
    
    @staticmethod
    def validate_port(port: int) -> bool:
        """Validate port number
        
        Args:
            port: Port number
        
        Returns:
            True if valid, False otherwise
        """
        return 1024 <= port <= 65535
    
    @staticmethod
    def validate_template(template: str) -> bool:
        """Validate template name
        
        Args:
            template: Template name
        
        Returns:
            True if valid, False otherwise
        """
        # Template names should be alphanumeric with underscores
        pattern = r'^[a-zA-Z0-9_]+$'
        return re.match(pattern, template) is not None
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username
        
        Args:
            username: Username
        
        Returns:
            True if valid, False otherwise
        """
        if not (3 <= len(username) <= 32):
            return False
        pattern = r'^[a-zA-Z0-9_-]+$'
        return re.match(pattern, username) is not None
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """Validate password strength
        
        Args:
            password: Password
        
        Returns:
            True if valid, False otherwise
        """
        if len(password) < 8:
            return False
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        return has_upper and has_lower and has_digit
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 256) -> str:
        """Sanitize string input
        
        Args:
            text: Text to sanitize
            max_length: Maximum length
        
        Returns:
            Sanitized string
        """
        # Remove null bytes
        text = text.replace('\x00', '')
        # Truncate
        text = text[:max_length]
        return text
    
    @staticmethod
    def sanitize_command(command: str) -> str:
        """Sanitize shell command
        
        Args:
            command: Command to sanitize
        
        Returns:
            Sanitized command
        """
        # Remove dangerous characters
        dangerous = ['&', '|', ';', '`', '$', '(', ')', '<', '>', '\n', '\r']
        for char in dangerous:
            command = command.replace(char, '')
        return command.strip()
    
    @staticmethod
    def is_safe_path(path: str) -> bool:
        """Check if path is safe (no path traversal)
        
        Args:
            path: File path
        
        Returns:
            True if safe, False otherwise
        """
        # Prevent path traversal
        if '..' in path or path.startswith('/'):
            return False
        return True


class InputValidator:
    """High-level input validator"""
    
    def __init__(self):
        """Initialize validator"""
        self.validators = Validators()
    
    def validate_credential(self, credential: dict) -> tuple:
        """Validate credential data
        
        Args:
            credential: Credential dictionary
        
        Returns:
            Tuple (valid: bool, errors: list)
        """
        errors = []
        
        if 'username' not in credential:
            errors.append("Missing username")
        elif not self.validators.validate_username(credential['username']):
            errors.append("Invalid username format")
        
        if 'password' not in credential:
            errors.append("Missing password")
        elif len(credential['password']) < 1:
            errors.append("Password cannot be empty")
        
        if 'email' in credential and credential['email']:
            if not self.validators.validate_email(credential['email']):
                errors.append("Invalid email format")
        
        return len(errors) == 0, errors
    
    def validate_config(self, config: dict) -> tuple:
        """Validate configuration
        
        Args:
            config: Configuration dictionary
        
        Returns:
            Tuple (valid: bool, errors: list)
        """
        errors = []
        
        if 'port' in config:
            if not self.validators.validate_port(config['port']):
                errors.append("Invalid port number")
        
        if 'template' in config:
            if not self.validators.validate_template(config['template']):
                errors.append("Invalid template name")
        
        return len(errors) == 0, errors
