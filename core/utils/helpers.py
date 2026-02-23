"""
SocialHook-X - Helper Utilities Module

Provides general purpose helper functions.
"""

import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class FileHelpers:
    """File operation helpers"""
    
    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Ensure directory exists
        
        Args:
            path: Directory path
        
        Returns:
            True if directory exists or created, False otherwise
        """
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creating directory {path}: {e}")
            return False
    
    @staticmethod
    def get_file_size(path: str) -> Optional[int]:
        """Get file size in bytes
        
        Args:
            path: File path
        
        Returns:
            File size or None
        """
        try:
            return os.path.getsize(path)
        except Exception as e:
            logger.error(f"Error getting file size: {e}")
            return None
    
    @staticmethod
    def list_files(directory: str, extension: str = None) -> List[str]:
        """List files in directory
        
        Args:
            directory: Directory path
            extension: Optional file extension filter
        
        Returns:
            List of file paths
        """
        try:
            files = []
            for item in Path(directory).iterdir():
                if item.is_file():
                    if extension is None or item.suffix == extension:
                        files.append(str(item))
            return files
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []
    
    @staticmethod
    def delete_file(path: str) -> bool:
        """Delete file
        
        Args:
            path: File path
        
        Returns:
            True if deleted, False otherwise
        """
        try:
            Path(path).unlink()
            return True
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False
    
    @staticmethod
    def read_file(path: str) -> Optional[str]:
        """Read file content
        
        Args:
            path: File path
        
        Returns:
            File content or None
        """
        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return None
    
    @staticmethod
    def write_file(path: str, content: str, append: bool = False) -> bool:
        """Write content to file
        
        Args:
            path: File path
            content: Content to write
            append: Append to file (True) or overwrite (False)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            mode = 'a' if append else 'w'
            with open(path, mode) as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error writing file: {e}")
            return False


class DataHelpers:
    """Data manipulation helpers"""
    
    @staticmethod
    def dict_to_sql_values(data: Dict) -> tuple:
        """Convert dictionary to SQL values tuple
        
        Args:
            data: Data dictionary
        
        Returns:
            Tuple (columns, placeholders, values)
        """
        columns = list(data.keys())
        placeholders = ','.join(['?' for _ in columns])
        values = tuple(data.values())
        return columns, placeholders, values
    
    @staticmethod
    def merge_dicts(*dicts) -> Dict:
        """Merge multiple dictionaries
        
        Args:
            *dicts: Dictionaries to merge
        
        Returns:
            Merged dictionary
        """
        result = {}
        for d in dicts:
            if d:
                result.update(d)
        return result
    
    @staticmethod
    def filter_dict(data: Dict, keys: List[str]) -> Dict:
        """Filter dictionary by keys
        
        Args:
            data: Dictionary to filter
            keys: Keys to keep
        
        Returns:
            Filtered dictionary
        """
        return {k: v for k, v in data.items() if k in keys}
    
    @staticmethod
    def flatten_dict(data: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """Flatten nested dictionary
        
        Args:
            data: Dictionary to flatten
            parent_key: Parent key prefix
            sep: Separator character
        
        Returns:
            Flattened dictionary
        """
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(DataHelpers.flatten_dict(v, new_key, sep).items())
            else:
                items.append((new_key, v))
        return dict(items)


class StringHelpers:
    """String manipulation helpers"""
    
    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate string to max length
        
        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix if truncated
        
        Returns:
            Truncated string
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def remove_duplicates(items: List[str]) -> List[str]:
        """Remove duplicates from list while preserving order
        
        Args:
            items: List of items
        
        Returns:
            List without duplicates
        """
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    @staticmethod
    def safe_encode(text: str) -> str:
        """Safely encode text to handle special characters
        
        Args:
            text: Text to encode
        
        Returns:
            Encoded string
        """
        return text.encode('utf-8', errors='replace').decode('utf-8')


class SystemHelpers:
    """System operation helpers"""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get system information
        
        Returns:
            System info dictionary
        """
        import platform
        import psutil
        
        return {
            "os": platform.system(),
            "os_release": platform.release(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total_gb": psutil.virtual_memory().total / (1024**3),
            "memory_available_gb": psutil.virtual_memory().available / (1024**3)
        }
    
    @staticmethod
    def get_memory_usage() -> Dict[str, float]:
        """Get memory usage statistics
        
        Returns:
            Memory usage dictionary
        """
        import psutil
        
        mem = psutil.virtual_memory()
        return {
            "total_gb": mem.total / (1024**3),
            "used_gb": mem.used / (1024**3),
            "available_gb": mem.available / (1024**3),
            "percent": mem.percent
        }
    
    @staticmethod
    def get_disk_usage(path: str = "/") -> Dict[str, float]:
        """Get disk usage statistics
        
        Args:
            path: Path to check
        
        Returns:
            Disk usage dictionary
        """
        import psutil
        
        disk = psutil.disk_usage(path)
        return {
            "total_gb": disk.total / (1024**3),
            "used_gb": disk.used / (1024**3),
            "free_gb": disk.free / (1024**3),
            "percent": disk.percent
        }
