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

# High-performance engines
from .async_engine import AsyncEngine, get_async_engine
from .threading_engine import ThreadingEngine, get_threading_engine

# Config submodules
from .config.templates import TemplateConfig
from .config.servers import ServerConfig

# Hooks submodules
from .hooks.events import EventHooks, get_event_hooks
from .hooks.webhooks import WebhookHandler, get_webhook_handler

# Utils submodules
from .utils.validators import Validators, InputValidator
from .utils.formatters import Formatters, CredentialFormatter
from .utils.helpers import FileHelpers, DataHelpers, StringHelpers, SystemHelpers

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
    'metadata', 'colors',
    # Engines
    'AsyncEngine', 'get_async_engine',
    'ThreadingEngine', 'get_threading_engine',
    # Config
    'TemplateConfig', 'ServerConfig',
    # Hooks
    'EventHooks', 'get_event_hooks',
    'WebhookHandler', 'get_webhook_handler',
    # Utils
    'Validators', 'InputValidator',
    'Formatters', 'CredentialFormatter',
    'FileHelpers', 'DataHelpers', 'StringHelpers', 'SystemHelpers'
]
