"""
SocialHook-X - Formatters Utility Module

Provides output formatting and data presentation functions.
"""

import logging
import html
from typing import Any, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class Formatters:
    """Output formatting utilities"""
    
    @staticmethod
    def format_credential(credential: Dict) -> str:
        """Format credential for display
        
        Args:
            credential: Credential dictionary
        
        Returns:
            Formatted string
        """
        lines = [
            f"Username: {credential.get('username', 'N/A')}",
            f"Password: {credential.get('password', 'N/A')}",
            f"Email: {credential.get('email', 'N/A')}",
            f"Browser: {credential.get('browser', 'N/A')}",
            f"OS: {credential.get('os', 'N/A')}",
            f"IP: {credential.get('ip', 'N/A')}",
            f"Country: {credential.get('country', 'N/A')}",
            f"Timestamp: {credential.get('timestamp', 'N/A')}"
        ]
        return "\n".join(lines)
    
    @staticmethod
    def format_table(headers: List[str], rows: List[List]) -> str:
        """Format data as table
        
        Args:
            headers: Column headers
            rows: Data rows
        
        Returns:
            Formatted table string
        """
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Build table
        lines = []
        
        # Header
        header_line = "  ".join(
            str(h).ljust(w) for h, w in zip(headers, col_widths)
        )
        lines.append(header_line)
        lines.append("-" * len(header_line))
        
        # Rows
        for row in rows:
            row_line = "  ".join(
                str(cell).ljust(w) for cell, w in zip(row, col_widths)
            )
            lines.append(row_line)
        
        return "\n".join(lines)
    
    @staticmethod
    def format_bytes(bytes_value: int) -> str:
        """Format bytes to human readable
        
        Args:
            bytes_value: Bytes value
        
        Returns:
            Formatted string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration to human readable
        
        Args:
            seconds: Duration in seconds
        
        Returns:
            Formatted string
        """
        if seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.2f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.2f}h"
    
    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Format datetime
        
        Args:
            dt: Datetime object
        
        Returns:
            Formatted string
        """
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def format_json(data: Any, indent: int = 2) -> str:
        """Format data as JSON
        
        Args:
            data: Data to format
            indent: Indentation level
        
        Returns:
            JSON string
        """
        import json
        return json.dumps(data, indent=indent, default=str)
    
    @staticmethod
    def format_stats(stats: Dict) -> str:
        """Format statistics for display
        
        Args:
            stats: Statistics dictionary
        
        Returns:
            Formatted string
        """
        lines = []
        for key, value in stats.items():
            # Convert key to readable format
            readable_key = key.replace('_', ' ').title()
            lines.append(f"{readable_key}: {value}")
        return "\n".join(lines)


class CredentialFormatter:
    """Credential-specific formatting"""
    
    @staticmethod
    def format_for_csv(credentials: List[Dict]) -> str:
        """Format credentials for CSV export
        
        Args:
            credentials: List of credentials
        
        Returns:
            CSV string
        """
        if not credentials:
            return ""
        
        import csv
        from io import StringIO
        
        output = StringIO()
        fieldnames = list(credentials[0].keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(credentials)
        
        return output.getvalue()
    
    @staticmethod
    def format_for_json(credentials: List[Dict]) -> str:
        """Format credentials for JSON export
        
        Args:
            credentials: List of credentials
        
        Returns:
            JSON string
        """
        import json
        return json.dumps(credentials, indent=2, default=str)
    
    @staticmethod
    def format_for_html_table(credentials: List[Dict]) -> str:
        """Format credentials as HTML table
        
        Args:
            credentials: List of credentials
        
        Returns:
            HTML string
        """
        if not credentials:
            return "<table></table>"
        
        html_table = "<table border='1' cellpadding='5'>\n"
        
        # Header
        fieldnames = list(credentials[0].keys())
        html_table += "  <tr>\n"
        for field in fieldnames:
            html_table += f"    <th>{html.escape(str(field))}</th>\n"
        html_table += "  </tr>\n"
        
        # Rows
        for cred in credentials:
            html_table += "  <tr>\n"
            for field in fieldnames:
                value = cred.get(field, '')
                html_table += f"    <td>{html.escape(str(value))}</td>\n"
            html_table += "  </tr>\n"
        
        html_table += "</table>"
        return html_table
    
    @staticmethod
    def format_summary(credentials: List[Dict]) -> str:
        """Format credential summary
        
        Args:
            credentials: List of credentials
        
        Returns:
            Summary string
        """
        lines = [
            f"Total Credentials: {len(credentials)}",
            f"Unique IPs: {len(set(c.get('ip', 'unknown') for c in credentials))}",
            f"Unique Browsers: {len(set(c.get('browser', 'unknown') for c in credentials))}",
        ]
        
        # Count by country
        countries = {}
        for cred in credentials:
            country = cred.get('country', 'Unknown')
            countries[country] = countries.get(country, 0) + 1
        
        lines.append("\nTop Countries:")
        for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True)[:5]:
            lines.append(f"  {country}: {count}")
        
        return "\n".join(lines)
