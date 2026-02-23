"""
SocialHook-X - ANSI Color Codes Module

Provides ANSI color codes for terminal output with bright blue aesthetic.
Supports bright colors, grey colors, background colors, and text styles.
"""

# Standard Colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Bright Colors
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Grey Scale Colors (various shades)
GREY_DARK = "\033[90m"          # Dark grey (bright black)
GREY_LIGHT = "\033[37m"         # Light grey (white)
GREY_MEDIUM = "\033[2m\033[37m" # Medium grey (dim white)

# Extended Grey Codes (256-color palette)
GREY_20 = "\033[38;5;236m"      # Very dark grey
GREY_40 = "\033[38;5;237m"      # Dark grey
GREY_60 = "\033[38;5;240m"      # Medium-dark grey
GREY_80 = "\033[38;5;244m"      # Medium grey
GREY_100 = "\033[38;5;248m"     # Medium-light grey
GREY_120 = "\033[38;5;250m"     # Light grey
GREY_140 = "\033[38;5;252m"     # Very light grey

# Background Colors (Standard)
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Background Colors (Bright)
BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"

# Text Styles
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"
HIDDEN = "\033[8m"
STRIKETHROUGH = "\033[9m"

# Reset
RESET = "\033[0m"

# Theme Colors (SocialHook-X Primary Color: Bright Blue & Green)
PRIMARY = BRIGHT_BLUE
SECONDARY = BRIGHT_GREEN
SUCCESS = BRIGHT_GREEN
WARNING = BRIGHT_YELLOW
ERROR = BRIGHT_RED
INFO = BRIGHT_BLUE
DEBUG = BRIGHT_MAGENTA
MUTED = GREY_MEDIUM

# Composite Styles
HEADER = f"{BRIGHT_BLUE}{BOLD}"
SUBHEADER = f"{BRIGHT_BLUE}{UNDERLINE}"
SUCCESS_TEXT = f"{BRIGHT_GREEN}{BOLD}"
ERROR_TEXT = f"{BRIGHT_RED}{BOLD}"
WARNING_TEXT = f"{BRIGHT_YELLOW}{BOLD}"
INFO_TEXT = f"{BRIGHT_BLUE}{BOLD}"

# Utility Functions
def colored(text: str, color: str = PRIMARY) -> str:
    """Apply color to text."""
    return f"{color}{text}{RESET}"

def bold(text: str, color: str = PRIMARY) -> str:
    """Apply bold color to text."""
    return f"{color}{BOLD}{text}{RESET}"

def header(text: str) -> str:
    """Format text as header."""
    return f"{HEADER}{text}{RESET}"

def subheader(text: str) -> str:
    """Format text as subheader."""
    return f"{SUBHEADER}{text}{RESET}"

def success(text: str) -> str:
    """Format text as success message."""
    return f"{SUCCESS_TEXT}{text}{RESET}"

def error(text: str) -> str:
    """Format text as error message."""
    return f"{ERROR_TEXT}{text}{RESET}"

def warning(text: str) -> str:
    """Format text as warning message."""
    return f"{WARNING_TEXT}{text}{RESET}"

def info(text: str) -> str:
    """Format text as info message."""
    return f"{INFO_TEXT}{text}{RESET}"

def debug(text: str) -> str:
    """Format text as debug message."""
    return f"{DEBUG}{BOLD}{text}{RESET}"

# Preformatted Messages
def format_title(title: str) -> str:
    """Format a title line."""
    return f"\n{BRIGHT_BLUE}{BOLD}{'═' * 60}{RESET}\n{BRIGHT_BLUE}{BOLD}{title}{RESET}\n{BRIGHT_BLUE}{BOLD}{'═' * 60}{RESET}\n"

def format_section(section: str) -> str:
    """Format a section header."""
    return f"\n{BRIGHT_BLUE}{BOLD}{section}{RESET}\n{BRIGHT_BLUE}{'─' * 60}{RESET}"

def format_menu_header(title: str) -> str:
    """Format menu header."""
    return f"{BRIGHT_BLUE}{BOLD}{title}{RESET}"

def format_menu_item(number: int, text: str) -> str:
    """Format menu item."""
    return f"  {BRIGHT_BLUE}[{number}]{RESET} {text}"

def format_option(option: str, description: str = "") -> str:
    """Format an option line."""
    if description:
        return f"  {BRIGHT_BLUE}{BOLD}→{RESET} {option}: {description}"
    return f"  {BRIGHT_BLUE}{BOLD}→{RESET} {option}"

# Box Drawing
def draw_box(title: str, content: list) -> str:
    """Draw a box with title and content."""
    box = f"{BRIGHT_BLUE}{BOLD}╔════════════════════════════════════════════════════════╗{RESET}\n"
    box += f"{BRIGHT_BLUE}{BOLD}║ {title:<54} ║{RESET}\n"
    box += f"{BRIGHT_BLUE}{BOLD}╚════════════════════════════════════════════════════════╝{RESET}\n"
    for line in content:
        box += f"  {line}\n"
    return box

def print_banner_line():
    """Print a banner separator line."""
    print(f"{BRIGHT_BLUE}{BOLD}{'═' * 60}{RESET}")

def print_section_line():
    """Print a section separator line."""
    print(f"{BRIGHT_BLUE}{'─' * 60}{RESET}")
