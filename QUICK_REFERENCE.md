# SocialHook-X - Quick Reference Card

## Metadata Module (`core/metadata.py`)

### Access Project Info
```python
from core import metadata

metadata.PROJECT_NAME          # "SocialHook-X"
metadata.PROJECT_VERSION       # "4.0.0"
metadata.AUTHOR                # "voltsparx"
metadata.AUTHOR_EMAIL          # "voltsparx@gmail.com"
metadata.REPOSITORY_URL        # "https://github.com/voltsparx/SocialHook-X"
metadata.LICENSE               # "MIT"
metadata.BUILD_DATE            # "February 23, 2026"
```

### Display Banners
```python
# Simple banner
metadata.print_banner()

# Full banner with features
metadata.print_full_banner()

# Get banner as string
banner = metadata.get_full_banner()
```

### Access Metadata
```python
metadata.FEATURES              # List of 10 key features
metadata.MODULES               # Dictionary of module metadata
metadata.VERSION_INFO          # Version breakdown (major, minor, patch)
```

---

## Colors Module (`core/colors.py`)

### Basic Colors
```python
from core import colors

# Standard colors
colors.RED, colors.GREEN, colors.BLUE, colors.YELLOW
colors.MAGENTA, colors.CYAN, colors.WHITE, colors.BLACK

# Bright versions (recommended)
colors.BRIGHT_RED
colors.BRIGHT_GREEN
colors.BRIGHT_BLUE          # ← Primary theme color
colors.BRIGHT_YELLOW
colors.BRIGHT_MAGENTA
colors.BRIGHT_CYAN
colors.BRIGHT_WHITE
colors.BRIGHT_BLACK
```

### Text Styles
```python
colors.BOLD                 # Make text bold
colors.DIM                  # Dim text
colors.ITALIC              # Italic text
colors.UNDERLINE           # Underlined text
colors.STRIKETHROUGH       # Strikethrough text
colors.REVERSE             # Reverse video
colors.HIDDEN              # Hidden text
colors.BLINK               # Blinking text
colors.RESET               # Reset all formatting
```

### Theme Colors
```python
colors.PRIMARY             # BRIGHT_BLUE (main color)
colors.SECONDARY           # CYAN
colors.SUCCESS             # BRIGHT_GREEN
colors.WARNING             # BRIGHT_YELLOW
colors.ERROR               # BRIGHT_RED
colors.INFO                # BRIGHT_BLUE
colors.DEBUG               # BRIGHT_MAGENTA
```

### Utility Functions
```python
# Simple coloring
colors.colored("text", colors.BRIGHT_BLUE)
colors.bold("text", colors.ERROR)

# Formatted messages
colors.success("Operation completed")
colors.error("Something failed")
colors.warning("Be careful")
colors.info("Information")
colors.debug("Debug output")

# Headers
colors.header("Main Title")
colors.subheader("Section Title")

# Menu formatting
colors.format_menu_header("Options")
colors.format_menu_item(1, "First option")
colors.format_menu_item(2, "Second option")
colors.format_option("--help", "Show help")

# Boxes
colors.draw_box("Title", ["Line 1", "Line 2", "Line 3"])
colors.format_title("Page Title")
colors.format_section("Section Header")

# Separators
colors.print_banner_line()      # Print ═══════════
colors.print_section_line()     # Print ─────────
```

---

## Common Usage Patterns

### Pattern 1: Display Project Banner on Startup
```python
from core import metadata

def main():
    metadata.print_full_banner()
    print("Starting SocialHook-X...")
```

### Pattern 2: Create Colored Menus
```python
from core import colors

def show_menu():
    print(colors.format_title("Main Menu"))
    print(colors.format_menu_item(1, "Option 1"))
    print(colors.format_menu_item(2, "Option 2"))
    print(colors.format_menu_item(0, "Exit"))
```

### Pattern 3: Display Status Messages
```python
from core import colors

print(colors.success("✓ Configuration loaded"))
print(colors.warning("⚠ No database found, creating..."))
print(colors.error("✗ Connection failed"))
print(colors.info("→ Processing request..."))
```

### Pattern 4: Format Application Output
```python
from core import colors

def process_credentials():
    print(colors.format_section("Credential Processing"))
    print(f"{colors.BRIGHT_BLUE}Total:{colors.RESET} 42")
    print(f"{colors.BRIGHT_BLUE}Success:{colors.RESET} 35")
    print(f"{colors.BRIGHT_BLUE}Failed:{colors.RESET} 7")
```

### Pattern 5: Colored F-String Output
```python
from core import colors

name = "SocialHook-X"
version = "4.0.0"

# Using color codes directly
output = f"{colors.BRIGHT_BLUE}{colors.BOLD}{name}{colors.RESET} v{version}"
print(output)

# Using utility functions
output = colors.bold(f"{name} v{version}", colors.BRIGHT_BLUE)
print(output)
```

---

## ANSI Color Codes Reference

| Element | Code | Usage |
|---------|------|-------|
| Bright Blue | `\033[94m` | Primary theme color |
| Cyan | `\033[36m` | Secondary color |
| Bright Green | `\033[92m` | Success/positive |
| Bright Yellow | `\033[93m` | Warning/caution |
| Bright Red | `\033[91m` | Error/negative |
| Bright Magenta | `\033[95m` | Debug/special |
| Bold | `\033[1m` | Text emphasis |
| Reset | `\033[0m` | Clear all formatting |

---

## Menu Structure

### Main Menu (show_main_menu)
```
═════════════════════════════ (BRIGHT_BLUE)
SOCIALHOOK-X MAIN MENU (BRIGHT_BLUE BOLD)
═════════════════════════════ (BRIGHT_BLUE)

[1] Select Phishing Template (BRIGHT_BLUE)
[2] Configure Tunnel (BRIGHT_BLUE)
[3] Set Custom Port (BRIGHT_BLUE)
[4] View Captured Data (BRIGHT_BLUE)
[5] Generate Reports (BRIGHT_BLUE)
[6] Email Notifications (BRIGHT_BLUE)
[7] Analytics Dashboard (BRIGHT_BLUE)
[8] System Info (BRIGHT_BLUE)
[0] Exit (BRIGHT_BLUE)
```

### Reports Menu (show_reports_menu)
```
═════════════════════════════ (BRIGHT_BLUE)
Report Generation (BRIGHT_BLUE BOLD)
═════════════════════════════ (BRIGHT_BLUE)

[1] Summary Report (BRIGHT_BLUE)
[2] Detailed Report (BRIGHT_BLUE)
[3] JSON Report (BRIGHT_BLUE)
[4] HTML Report (BRIGHT_BLUE)
[5] Generate All Reports (BRIGHT_BLUE)
```

---

## File Locations

```
core/
├── metadata.py          ← Project metadata
├── colors.py            ← ANSI color codes
├── __init__.py          ← Updated with imports
└── [other modules]

socialhook-x.py          ← Main app using metadata & colors
METADATA_COLORS_GUIDE.md ← Complete documentation
```

---

## Integration Points

### In socialhook-x.py
```python
# Imports
from core import metadata, colors

# Display banner
metadata.print_full_banner()

# Use colors in menus
print(f"{colors.BRIGHT_BLUE}[1]{colors.RESET} Option")

# Access metadata
print(f"Project: {metadata.PROJECT_NAME} v{metadata.PROJECT_VERSION}")
print(f"Author: {metadata.AUTHOR}")
```

---

## Color Combinations for UI Elements

### Headers
```python
f"{colors.BRIGHT_BLUE}{colors.BOLD}═══════════════{colors.RESET}"
```

### Menu Items
```python
f"{colors.BRIGHT_BLUE}[1]{colors.RESET} Menu Item"
```

### Section Labels
```python
f"{colors.BRIGHT_BLUE}{colors.BOLD}Section Name:{colors.RESET}"
```

### Status Indicators
```python
colors.success("✓ Success")
colors.error("✗ Error")
colors.warning("⚠ Warning")
colors.info("→ Info")
```

---

## Best Practices

1. **Always use RESET** after color codes
   ```python
   print(f"{colors.BRIGHT_BLUE}Text{colors.RESET} Normal text")
   ```

2. **Use utility functions** for consistency
   ```python
   colors.success("Done")  # Better than manual color codes
   ```

3. **Combine colors with styles** for impact
   ```python
   f"{colors.BRIGHT_BLUE}{colors.BOLD}Important{colors.RESET}"
   ```

4. **Access metadata centrally**
   ```python
   from core import metadata
   print(metadata.PROJECT_VERSION)
   ```

5. **Use theme colors** instead of hardcoding
   ```python
   colors.ERROR  # Use theme color
   colors.BRIGHT_RED  # Avoid hardcoding
   ```

---

## Quick Copy-Paste Templates

### Colored Output
```python
from core import colors

print(colors.success("Operation completed successfully"))
print(colors.error("An error occurred"))
print(colors.warning("Warning: This action cannot be undone"))
print(colors.info("Processing..."))
```

### Menu Display
```python
from core import colors

print(colors.format_title("My Menu"))
print(colors.format_menu_item(1, "First Option"))
print(colors.format_menu_item(2, "Second Option"))
print(colors.format_menu_item(0, "Exit"))
```

### Project Info
```python
from core import metadata

print(f"{metadata.PROJECT_NAME} v{metadata.PROJECT_VERSION}")
print(f"By {metadata.AUTHOR}")
print(f"Repository: {metadata.REPOSITORY_URL}")
```

### Banner Display
```python
from core import metadata

metadata.print_full_banner()
```

---

**Last Updated:** February 23, 2026  
**Version:** 4.0.0  
**Status:** Production Ready
