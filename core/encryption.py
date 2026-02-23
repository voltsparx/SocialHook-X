"""
SocialHook-X - Encryption Module
Provides encryption/decryption for sensitive data at rest
"""

import os
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf import pbkdf2
import base64
from typing import Optional

logger = logging.getLogger(__name__)


class CredentialEncryption:
    """Encrypt and decrypt sensitive credential data"""
    
    def __init__(self, master_key: Optional[str] = None):
        """Initialize encryption
        
        Args:
            master_key: Master encryption key (generated if not provided)
        """
        if master_key:
            self.cipher = Fernet(master_key.encode() if isinstance(master_key, str) else master_key)
        else:
            self.cipher = Fernet(Fernet.generate_key())
        
        logger.info("Encryption cipher initialized")
    
    @staticmethod
    def generate_key() -> str:
        """Generate new encryption key
        
        Returns:
            Base64-encoded encryption key
        """
        return Fernet.generate_key().decode()
    
    @staticmethod
    def derive_key_from_password(password: str, salt: Optional[bytes] = None) -> tuple:
        """Derive encryption key from password
        
        Args:
            password: Password to derive from
            salt: Salt (generated if not provided)
        
        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = pbkdf2.PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key.decode(), base64.b64encode(salt).decode()
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data
        
        Args:
            data: Data to encrypt
        
        Returns:
            Encrypted data (base64)
        """
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return base64.b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return None
    
    def decrypt(self, encrypted_data: str) -> Optional[str]:
        """Decrypt data
        
        Args:
            encrypted_data: Encrypted data (base64)
        
        Returns:
            Decrypted string or None
        """
        try:
            encrypted = base64.b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return None
    
    def encrypt_dict(self, data: dict, fields: list) -> dict:
        """Encrypt specific fields in dict
        
        Args:
            data: Dictionary to encrypt
            fields: List of field names to encrypt
        
        Returns:
            Dictionary with encrypted fields
        """
        result = data.copy()
        for field in fields:
            if field in result and result[field]:
                result[field] = self.encrypt(str(result[field]))
        return result
    
    def decrypt_dict(self, data: dict, fields: list) -> dict:
        """Decrypt specific fields in dict
        
        Args:
            data: Dictionary to decrypt
            fields: List of field names to decrypt
        
        Returns:
            Dictionary with decrypted fields
        """
        result = data.copy()
        for field in fields:
            if field in result and result[field]:
                result[field] = self.decrypt(result[field])
        return result
