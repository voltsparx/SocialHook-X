# SocialHook-X - Metadata & Colors Integration Guide

## Overview

SocialHook-X v4.0 now includes a comprehensive metadata system and ANSI color theming with **bright blue** as the primary aesthetic color.

## Files Created

### 1. `core/metadata.py` (Project Metadata Module)

Contains all project metadata including version, author, and repository information.

**Key Variables:**
```python
PROJECT_NAME = "SocialHook-X"
PROJECT_VERSION = "4.0.0"
AUTHOR = "voltsparx"
AUTHOR_EMAIL = "voltsparx@gmail.com"
REPOSITORY_URL = "https://github.com/voltsparx/SocialHook-X"
```

**Key Functions:**

| Function | Purpose |
|----------|---------|
| `get_version()` | Returns formatted version string |
| `get_banner()` | Returns simple project banner |
| `get_full_banner()` | Returns detailed banner with features |
| `print_banner()` | Prints simple banner to console |
| `print_full_banner()` | Prints detailed banner to console |

**Usage Examples:**

```python
from core import metadata

# Display version
print(metadata.get_version())
# Output: SocialHook-X v4.0.0

# Display full banner with features
metadata.print_full_banner()

# Access project information
print(f"Author: {metadata.AUTHOR}")
print(f"Repository: {metadata.REPOSITORY_URL}")
print(f"Features: {', '.join(metadata.FEATURES)}")
```

---

### 2. `core/colors.py` (ANSI Color Codes Module)

Provides ANSI color codes for terminal output with bright blue as the primary theme.

**Color Categories:**

**Basic Colors:**
```python
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
```

**Bright Colors:**
```python
BRIGHT_BLACK, BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW
BRIGHT_BLUE, BRIGHT_MAGENTA, BRIGHT_CYAN, BRIGHT_WHITE
```

**Text Styles:**
```python
BOLD, DIM, ITALIC, UNDERLINE, BLINK, REVERSE, HIDDEN, STRIKETHROUGH
```

**Theme Colors (SocialHook-X):**
```python
PRIMARY = BRIGHT_BLUE          # Main theme color
SECONDARY = CYAN              # Secondary color
SUCCESS = BRIGHT_GREEN        # Success messages
WARNING = BRIGHT_YELLOW       # Warning messages
ERROR = BRIGHT_RED            # Error messages
INFO = BRIGHT_BLUE            # Info messages
DEBUG = BRIGHT_MAGENTA        # Debug messages
```

**Reset:**
```python
RESET = "\033[0m"             # Reset all formatting
```

**Utility Functions:**

| Function | Purpose | Example |
|----------|---------|---------|
| `colored(text, color)` | Apply color to text | `colored("Hello", BRIGHT_BLUE)` |
| `bold(text, color)` | Apply bold color | `bold("Alert", ERROR)` |
| `header(text)` | Format as header | `header("Section Title")` |
| `subheader(text)` | Format as subheader | `subheader("Subsection")` |
| `success(text)` | Format as success | `success("Operation completed")` |
| `error(text)` | Format as error | `error("Something went wrong")` |
| `warning(text)` | Format as warning | `warning("Be careful")` |
| `info(text)` | Format as info | `info("Information")` |
| `debug(text)` | Format as debug | `debug("Debug info")` |

**Box Drawing Functions:**

```python
format_title(title)         # Format title with borders
format_section(section)     # Format section header
format_menu_header(title)   # Format menu header
format_menu_item(num, text) # Format menu item
format_option(option, desc) # Format option line
draw_box(title, content)    # Draw a bordered box
print_banner_line()         # Print banner separator
print_section_line()        # Print section separator
```

**Usage Examples:**

```python
from core import colors

# Basic colored text
print(colors.colored("Hello", colors.BRIGHT_BLUE))

# Bold with color
print(colors.bold("Important!", colors.ERROR))

# Formatted messages
print(colors.success("Task completed!"))
print(colors.error("An error occurred"))
print(colors.warning("Warning message"))

# Menu formatting
print(colors.format_menu_header("Main Menu"))
print(colors.format_menu_item(1, "Option 1"))
print(colors.format_menu_item(2, "Option 2"))

# Box drawing
content = ["Line 1", "Line 2", "Line 3"]
print(colors.draw_box("Title", content))

# Headers and sections
print(colors.format_title("Main Title"))
print(colors.format_section("Section Header"))
```

---

## Integration in Main Application

### socialhook-x.py Changes

The main application now imports and uses both modules:

```python
from core import metadata, colors

class SocialHookX:
    def print_banner(self):
        """Print application banner"""
        metadata.print_full_banner()
    
    def show_main_menu(self):
        """Display main menu with bright blue theme"""
        print(f"\n{colors.BRIGHT_BLUE}{colors.BOLD}╔════════════════════════════════════════╗{colors.RESET}")
        print(f"{colors.BRIGHT_BLUE}{colors.BOLD}║{colors.RESET} {colors.BRIGHT_BLUE}{colors.BOLD}SOCIALHOOK-X MAIN MENU{colors.RESET:^36} {colors.BRIGHT_BLUE}{colors.BOLD}║{colors.RESET}")
        print(f"{colors.BRIGHT_BLUE}{colors.BOLD}╚════════════════════════════════════════╝{colors.RESET}\n")
        
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}1{colors.BRIGHT_BLUE}]{colors.RESET} Select Phishing Template")
        # ... more menu items
```

### All Updated Menus

The following menus now use bright blue aesthetic:

| Menu | Location | Features |
|------|----------|----------|
| **Main Menu** | `show_main_menu()` | Bright blue headers and items |
| **Template Selection** | `show_templates_menu()` | Bright blue formatting |
| **Reports** | `show_reports_menu()` | Bright blue section headers |
| **Email Setup** | `setup_email_notifications()` | Bright blue input prompts |
| **Analytics** | `show_analytics_dashboard()` | Bright blue labels |
| **System Info** | `show_system_info()` | Metadata integration, bright blue |
| **Captured Data** | `view_captured_data()` | Bright blue section headers |

---

## Color Scheme Reference

### Primary Color (Bright Blue)
```
ANSI Code: \033[94m
Used for: Headers, menu items, borders, main UI elements
```

### Accent Colors
```
Success (Bright Green):    \033[92m
Warning (Bright Yellow):   \033[93m
Error (Bright Red):        \033[91m
Info (Bright Blue):        \033[94m
Debug (Bright Magenta):    \033[95m
```

### Example Output

```
╔════════════════════════════════════════╗
║         SOCIALHOOK-X MAIN MENU         ║  ← Bright Blue Bold
╚════════════════════════════════════════╝

[1] Select Phishing Template             ← Bright Blue
[2] Configure Tunnel                     ← Bright Blue
[3] Set Custom Port                      ← Bright Blue
[0] Exit                                 ← Bright Blue
```

---

## Project Metadata Structure

```python
PROJECT_NAME = "SocialHook-X"
PROJECT_VERSION = "4.0.0"
PROJECT_DESCRIPTION = "Professional Phishing Framework with Advanced Analytics"

AUTHOR = "voltsparx"
AUTHOR_EMAIL = "voltsparx@gmail.com"
AUTHOR_CONTACT = "voltsparx <voltsparx@gmail.com>"

REPOSITORY_URL = "https://github.com/voltsparx/SocialHook-X"
REPOSITORY_ISSUES = "https://github.com/voltsparx/SocialHook-X/issues"
REPOSITORY_WIKI = "https://github.com/voltsparx/SocialHook-X/wiki"

LICENSE = "MIT"
LICENSE_YEAR = "2026"
BUILD_DATE = "February 23, 2026"
BUILD_STATUS = "Production Ready"

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
```

---

## Module Metadata

Each core module has metadata in the `MODULES` dictionary:

```python
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
    # ... more modules
}
```

---

## Version Information

```python
VERSION_INFO = {
    "major": 4,
    "minor": 0,
    "patch": 0,
    "status": "stable"
}
```

---

## Usage in Your Code

### Example 1: Display Project Banner on Startup

```python
from core import metadata

def main():
    metadata.print_full_banner()
    print("Starting application...")
```

### Example 2: Use Colors in Custom Menus

```python
from core import colors

def custom_menu():
    print(colors.format_title("My Custom Menu"))
    print(colors.format_menu_header("Options"))
    print(colors.format_menu_item(1, "First option"))
    print(colors.format_menu_item(2, "Second option"))
    print(colors.format_menu_item(0, "Exit"))
```

### Example 3: Add Colored Output to Functions

```python
from core import colors

def process_data():
    print(colors.success("Data processed successfully!"))
    print(colors.info("Waiting for user input..."))
    print(colors.warning("This may take a while"))
    print(colors.error("Critical error occurred!"))
```

### Example 4: Access Project Info

```python
from core import metadata

print(f"Using {metadata.PROJECT_NAME} v{metadata.PROJECT_VERSION}")
print(f"Author: {metadata.AUTHOR}")
print(f"Repository: {metadata.REPOSITORY_URL}")
```

---

## Benefits

✅ **Centralized Metadata** - Single source of truth for project information  
✅ **Consistent Theming** - Bright blue aesthetic throughout the application  
✅ **Easy Maintenance** - Update version/author in one place  
✅ **Professional Appearance** - ANSI colors for polished terminal UI  
✅ **Code Reusability** - Import and use colors/metadata anywhere  
✅ **Type Safe** - String constants prevent typos  
✅ **Readable Code** - F-strings with named color constants  

---

## Files Modified

- ✅ `core/metadata.py` - Created (New)
- ✅ `core/colors.py` - Created (New)
- ✅ `core/__init__.py` - Updated (Added imports)
- ✅ `socialhook-x.py` - Updated (Using metadata & colors in menus)

---

## Compilation Status

✅ All Python files compile successfully  
✅ No syntax errors  
✅ Ready for production  

---

**Last Updated:** February 23, 2026  
**Version:** 4.0.0  
**Status:** Production Ready
