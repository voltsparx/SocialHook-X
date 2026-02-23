"""
SocialHook-X Core Package
Main application framework and utilities
"""

from .config import Config, DevelopmentConfig, ProductionConfig
from .utils import (
    Colors, TemplateManager, Logger, 
    print_header, print_success, print_error, print_info, print_warning,
    command_exists, run_command, get_os_type, get_architecture,
    save_to_output, load_json_file, get_timestamp
)
from .database import CredentialDB
from .webserver import WebServer
from .notifications import EmailNotifier, AlertManager
from .geolocation import GeoLocationTracker, IPAnalyzer
from .reports import ReportGenerator
from . import metadata
from . import colors

__version__ = "4.0"
__author__ = "SocialHook-X Team"
__all__ = [
    'Config', 'DevelopmentConfig', 'ProductionConfig',
    'Colors', 'TemplateManager', 'Logger',
    'print_header', 'print_success', 'print_error', 'print_info', 'print_warning',
    'command_exists', 'run_command', 'get_os_type', 'get_architecture',
    'save_to_output', 'load_json_file', 'get_timestamp',
    'CredentialDB', 'WebServer', 
    'EmailNotifier', 'AlertManager',
    'GeoLocationTracker', 'IPAnalyzer',
    'ReportGenerator',
    'metadata', 'colors'
]
