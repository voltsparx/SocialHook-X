"""
SocialHook-X Geolocation Module
IP geolocation tracking and caching
"""

import requests
import logging
from typing import Dict, Optional
import time

logger = logging.getLogger(__name__)

class GeoLocationTracker:
    """Track and cache geolocation data for IPs"""
    
    def __init__(self, db = None):
        self.db = db
        self.cache = {}
        self.api_calls = 0
        self.last_api_call = 0
        self.rate_limit = 1  # seconds between API calls
    
    def set_database(self, db):
        """Set database for caching"""
        self.db = db
    
    def get_location(self, ip_address: str, use_cache: bool = True) -> Optional[Dict]:
        """Get geolocation data for IP"""
        
        # Skip localhost
        if ip_address in ['127.0.0.1', 'localhost', '::1']:
            return {
                'ip': ip_address,
                'country': 'Localhost',
                'city': 'Local',
                'latitude': 0,
                'longitude': 0,
                'isp': 'Local Network'
            }
        
        # Check memory cache
        if use_cache and ip_address in self.cache:
            return self.cache[ip_address]
        
        # Check database cache
        if use_cache and self.db:
            cached = self.db.get_cached_geo(ip_address)
            if cached:
                self.cache[ip_address] = cached
                return cached
        
        # Fetch from API
        geo_data = self._fetch_from_api(ip_address)
        
        if geo_data:
            # Cache in memory
            self.cache[ip_address] = geo_data
            
            # Cache in database
            if self.db:
                self.db.cache_geo_data(ip_address, geo_data)
        
        return geo_data
    
    def _fetch_from_api(self, ip_address: str) -> Optional[Dict]:
        """Fetch geolocation from API"""
        
        # Rate limiting
        time_since_last = time.time() - self.last_api_call
        if time_since_last < self.rate_limit:
            time.sleep(self.rate_limit - time_since_last)
        
        try:
            # Try geoip-db.com API
            url = f'https://geoip-db.com/json/{ip_address}'
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                geo_data = {
                    'ip': ip_address,
                    'country': data.get('country_name', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'latitude': data.get('latitude', 0),
                    'longitude': data.get('longitude', 0),
                    'isp': data.get('isp', 'Unknown'),
                    'state': data.get('state', '')
                }
                
                self.api_calls += 1
                self.last_api_call = time.time()
                
                logger.info(f"Geolocation fetched: {ip_address} -> {geo_data.get('city')}, {geo_data.get('country')}")
                return geo_data
        
        except requests.exceptions.Timeout:
            logger.warning(f"Geolocation API timeout for {ip_address}")
        except requests.exceptions.ConnectionError:
            logger.warning(f"Geolocation API connection error for {ip_address}")
        except Exception as e:
            logger.error(f"Error fetching geolocation for {ip_address}: {e}")
        
        # Return empty geolocation on failure
        return {
            'ip': ip_address,
            'country': 'Unknown',
            'city': 'Unknown',
            'latitude': 0,
            'longitude': 0,
            'isp': 'Unknown'
        }
    
    def get_stats(self) -> Dict:
        """Get geolocation stats"""
        return {
            'cache_size': len(self.cache),
            'api_calls': self.api_calls,
            'cached_ips': list(self.cache.keys())
        }


class IPAnalyzer:
    """Analyze IP addresses and detect patterns"""
    
    def __init__(self, geo_tracker: GeoLocationTracker = None):
        self.geo_tracker = geo_tracker or GeoLocationTracker()
        self.ip_list = []
    
    def analyze_ip(self, ip_address: str) -> Dict:
        """Analyze single IP"""
        
        geo_data = self.geo_tracker.get_location(ip_address)
        
        analysis = {
            'ip': ip_address,
            'geolocation': geo_data,
            'is_private': self._is_private_ip(ip_address),
            'is_vpn_likely': self._is_vpn_likely(geo_data),
            'risk_score': self._calculate_risk_score(geo_data)
        }
        
        return analysis
    
    def analyze_batch(self, ip_addresses: list) -> list:
        """Analyze multiple IPs"""
        
        analyses = []
        for ip in ip_addresses:
            analyses.append(self.analyze_ip(ip))
        
        return analyses
    
    def _is_private_ip(self, ip: str) -> bool:
        """Check if IP is private"""
        private_ranges = [
            '10.',
            '172.16.',
            '192.168.',
            '127.',
            '169.254.'
        ]
        
        for range_start in private_ranges:
            if ip.startswith(range_start):
                return True
        
        return False
    
    def _is_vpn_likely(self, geo_data: Dict) -> bool:
        """Heuristic check if IP might be VPN"""
        
        # VPN providers often have generic ISP names
        vpn_indicators = ['VPN', 'proxy', 'hosting', 'cloud', 'datacenter']
        isp = (geo_data.get('isp', '') or '').lower()
        
        for indicator in vpn_indicators:
            if indicator.lower() in isp:
                return True
        
        return False
    
    def _calculate_risk_score(self, geo_data: Dict) -> float:
        """Calculate risk score (0-100)"""
        
        score = 0.0
        
        # Location unknown = higher risk
        if geo_data.get('country') == 'Unknown':
            score += 30
        
        # ISP unknown = higher risk
        if geo_data.get('isp') == 'Unknown':
            score += 20
        
        # VPN likely = moderate risk
        if self._is_vpn_likely(geo_data):
            score += 25
        
        return min(score, 100)
