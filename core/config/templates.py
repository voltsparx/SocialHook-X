"""
SocialHook-X - Templates Configuration Module

Manages template configuration, templates list, and template metadata.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class TemplateConfig:
    """Template configuration manager"""
    
    TEMPLATES = {
        "facebook": {"name": "Facebook", "category": "Social Media"},
        "instagram": {"name": "Instagram", "category": "Social Media"},
        "google": {"name": "Google", "category": "Services"},
        "microsoft": {"name": "Microsoft", "category": "Services"},
        "github": {"name": "GitHub", "category": "Development"},
        "linkedin": {"name": "LinkedIn", "category": "Professional"},
        "twitter": {"name": "Twitter", "category": "Social Media"},
        "amazon": {"name": "Amazon", "category": "E-commerce"},
        "paypal": {"name": "PayPal", "category": "Payment"},
        "discord": {"name": "Discord", "category": "Communication"},
        "netflix": {"name": "Netflix", "category": "Streaming"},
        "twitch": {"name": "Twitch", "category": "Streaming"},
        "steam": {"name": "Steam", "category": "Gaming"},
        "roblox": {"name": "Roblox", "category": "Gaming"},
        "snapchat": {"name": "Snapchat", "category": "Social Media"},
        "tiktok": {"name": "TikTok", "category": "Social Media"},
        "reddit": {"name": "Reddit", "category": "Social Media"},
        "quora": {"name": "Quora", "category": "Q&A"},
        "spotify": {"name": "Spotify", "category": "Streaming"},
        "dropbox": {"name": "Dropbox", "category": "Cloud"},
    }
    
    @classmethod
    def get_template_list(cls) -> List[Tuple[int, str, str]]:
        """Get list of available templates
        
        Returns:
            List of tuples (number, key, name)
        """
        templates = []
        for idx, (key, config) in enumerate(cls.TEMPLATES.items(), 1):
            templates.append((idx, key, config["name"]))
        return templates
    
    @classmethod
    def get_templates_by_category(cls, category: str) -> Dict[str, str]:
        """Get templates by category
        
        Args:
            category: Template category
        
        Returns:
            Dictionary of templates in category
        """
        return {
            key: config["name"]
            for key, config in cls.TEMPLATES.items()
            if config.get("category") == category
        }
    
    @classmethod
    def get_categories(cls) -> List[str]:
        """Get all template categories
        
        Returns:
            List of categories
        """
        categories = set()
        for config in cls.TEMPLATES.values():
            categories.add(config.get("category"))
        return sorted(list(categories))
    
    @classmethod
    def validate_template(cls, template: str) -> bool:
        """Validate template exists
        
        Args:
            template: Template key
        
        Returns:
            True if valid, False otherwise
        """
        return template in cls.TEMPLATES
    
    @classmethod
    def get_template_info(cls, template: str) -> Optional[Dict]:
        """Get template information
        
        Args:
            template: Template key
        
        Returns:
            Template info dictionary or None
        """
        return cls.TEMPLATES.get(template)
    
    @classmethod
    def get_template_count(cls) -> int:
        """Get total template count
        
        Returns:
            Number of templates
        """
        return len(cls.TEMPLATES)
