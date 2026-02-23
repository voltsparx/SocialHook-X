#!/usr/bin/env python3
"""
SocialHook-X Installer
Automated installation and setup
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class Installer:
    """SocialHook-X Installation Manager"""
    
    def __init__(self):
        self.os_type = self.detect_os()
        self.success_count = 0
        self.failed_count = 0
    
    def detect_os(self) -> str:
        """Detect operating system"""
        system = platform.system().lower()
        if 'linux' in system:
            return 'linux'
        elif 'darwin' in system:
            return 'macos'
        else:
            return 'unknown'
    
    def print_status(self, msg: str, status: str = 'info'):
        """Print status message"""
        colors = {
            'info': '\033[0;94m',
            'success': '\033[0;92m',
            'error': '\033[0;91m',
            'warning': '\033[0;93m',
            'reset': '\033[0m'
        }
        
        symbols = {
            'info': '[*]',
            'success': '[+]',
            'error': '[!]',
            'warning': '[!]'
        }
        
        color = colors.get(status, colors['info'])
        symbol = symbols.get(status, '[*]')
        
        print(f"{color}{symbol} {msg}{colors['reset']}")
        
        if status == 'success':
            self.success_count += 1
        elif status == 'error':
            self.failed_count += 1
    
    def run_command(self, cmd: str) -> bool:
        """Run shell command"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def check_command(self, cmd: str) -> bool:
        """Check if command exists"""
        return self.run_command(f"which {cmd} > /dev/null 2>&1")
    
    def print_banner(self):
        """Print installer banner"""
        print("\033[0;94m" + "="*60 + "\033[0m")
        print("\033[0;96m")
        print("""
    ███████  ██████   ██████  ██   ██  █████  ██      
    ██       ██    ██ ██      ██  ██  ██   ██ ██      
    ███████  ██    ██ ██      █████   ███████ ██      
         ██ ██    ██ ██      ██  ██  ██   ██ ██      
    ███████  ██████   ██████ ██   ██ ██   ██ ███████ 
    
    SocialHook-X Installer
        """)
        print("\033[0m")
        print("\033[0;94m" + "="*60 + "\033[0m\n")
    
    def check_dependencies(self):
        """Check required dependencies"""
        self.print_status("Checking dependencies...")
        
        required = ['python3', 'php', 'curl', 'wget']
        missing = []
        
        for cmd in required:
            if self.check_command(cmd):
                self.print_status(f"{cmd} found", 'success')
            else:
                self.print_status(f"{cmd} not found", 'warning')
                missing.append(cmd)
        
        if missing:
            self.print_status(f"Please install: {', '.join(missing)}", 'warning')
            return False
        
        return True
    
    def install_python_packages(self):
        """Install Python packages"""
        self.print_status("Installing Python packages...")
        
        packages = [
            'flask>=2.3.0',
            'requests>=2.31.0',
            'colorama>=0.4.6',
            'python-dotenv>=1.0.0',
        ]
        
        for package in packages:
            self.print_status(f"Installing {package}...")
            if self.run_command(f"{sys.executable} -m pip install {package}"):
                self.print_status(f"{package} installed", 'success')
            else:
                self.print_status(f"Failed to install {package}", 'warning')
    
    def install_system_dependencies(self):
        """Install system dependencies"""
        self.print_status("Installing system dependencies...")
        
        if self.os_type == 'linux':
            # Detect package manager
            if self.check_command('apt-get'):
                self.print_status("Using apt-get...")
                self.run_command('sudo apt-get update')
                self.run_command('sudo apt-get install -y php php-curl php-cli curl wget')
            elif self.check_command('yum'):
                self.print_status("Using yum...")
                self.run_command('sudo yum install -y php php-curl php-cli curl wget')
            elif self.check_command('dnf'):
                self.print_status("Using dnf...")
                self.run_command('sudo dnf install -y php php-curl php-cli curl wget')
            else:
                self.print_status("Package manager not detected", 'warning')
        
        elif self.os_type == 'macos':
            if self.check_command('brew'):
                self.print_status("Using brew...")
                self.run_command('brew install php curl wget')
            else:
                self.print_status("Homebrew not found", 'warning')
    
    def setup_directories(self):
        """Setup required directories"""
        self.print_status("Setting up directories...")
        
        dirs = ['core', 'templates', 'servers', 'output', 'captured_data']
        
        for d in dirs:
            path = Path(d)
            path.mkdir(exist_ok=True)
            self.print_status(f"Directory ready: {d}", 'success')
    
    def create_config_file(self):
        """Create configuration file"""
        self.print_status("Creating configuration...")
        
        config_content = """# SocialHook-X Configuration
SHX_ENV=development
SHX_HOST=127.0.0.1
SHX_PORT=8080
SHX_DEBUG=False
SHX_LOG_LEVEL=INFO
SHX_DEFAULT_TUNNEL=localhost
SHX_TUNNEL_TIMEOUT=30
"""
        
        config_file = Path('.env')
        if not config_file.exists():
            with open(config_file, 'w') as f:
                f.write(config_content)
            self.print_status("Configuration file created", 'success')
        else:
            self.print_status("Configuration file already exists", 'info')
    
    def create_requirements_file(self):
        """Create requirements.txt"""
        self.print_status("Creating requirements.txt...")
        
        requirements = """# SocialHook-X Requirements
Flask>=2.3.0
Werkzeug>=2.3.0
Jinja2>=3.1.0
requests>=2.31.0
colorama>=0.4.6
python-dotenv>=1.0.0
"""
        
        req_file = Path('requirements.txt')
        if not req_file.exists():
            with open(req_file, 'w') as f:
                f.write(requirements)
            self.print_status("requirements.txt created", 'success')
        else:
            self.print_status("requirements.txt already exists", 'info')
    
    def set_permissions(self):
        """Set file permissions"""
        self.print_status("Setting file permissions...")
        
        scripts = ['socialhook-x.py', 'install-socialhook.py']
        
        for script in scripts:
            script_path = Path(script)
            if script_path.exists():
                os.chmod(script_path, 0o755)
                self.print_status(f"Permissions set: {script}", 'success')
    
    def run(self):
        """Run installation"""
        self.print_banner()
        
        if self.os_type == 'unknown':
            self.print_status("Unsupported OS", 'error')
            return 1
        
        self.print_status(f"Detected OS: {self.os_type.upper()}")
        
        # Installation steps
        if not self.check_dependencies():
            self.print_status("Dependency check failed", 'warning')
        
        self.install_system_dependencies()
        self.install_python_packages()
        self.setup_directories()
        self.create_config_file()
        self.create_requirements_file()
        self.set_permissions()
        
        # Summary
        print("\n" + "\033[0;94m" + "="*60 + "\033[0m")
        self.print_status(f"Installation complete!", 'success')
        self.print_status(f"Successful: {self.success_count}", 'success')
        if self.failed_count > 0:
            self.print_status(f"Failed: {self.failed_count}", 'warning')
        print("\033[0;94m" + "="*60 + "\033[0m")
        
        print("\n\033[0;92mNext steps:\033[0m")
        print("  1. python3 socialhook-x.py")
        print("  2. Select a template")
        print("  3. Configure tunnel")
        print("  4. Monitor for credentials\n")
        
        return 0

def main():
    """Main entry point"""
    installer = Installer()
    return installer.run()

if __name__ == '__main__':
    sys.exit(main())
