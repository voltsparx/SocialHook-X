#!/usr/bin/env python3
"""
SocialHook-X v4.0 - Quick Start Guide
Run this to verify the installation and get started
"""

import os
import sys
from pathlib import Path

def print_header(text):
    """Print colored header"""
    print(f"\033[94m{'='*60}\033[0m")
    print(f"\033[96m{text:^60}\033[0m")
    print(f"\033[94m{'='*60}\033[0m\n")

def print_success(text):
    """Print success message"""
    print(f"\033[92m[+]\033[0m {text}")

def print_error(text):
    """Print error message"""
    print(f"\033[91m[!]\033[0m {text}")

def print_info(text):
    """Print info message"""
    print(f"\033[94m[*]\033[0m {text}")

def verify_structure():
    """Verify project structure"""
    print_header("VERIFYING PROJECT STRUCTURE")
    
    required_dirs = [
        'core', 'templates', 'servers', 'captured_data', 'output', 'third_party'
    ]
    
    required_files = [
        'socialhook-x.py', 'install-socialhook.py', 'requirements.txt',
        '.env.example', 'README.md'
    ]
    
    all_ok = True
    
    print("Directories:")
    for d in required_dirs:
        path = Path(d)
        if path.exists() and path.is_dir():
            print_success(f"{d}/")
        else:
            print_error(f"{d}/ - MISSING")
            all_ok = False
    
    print("\nFiles:")
    for f in required_files:
        path = Path(f)
        if path.exists() and path.is_file():
            print_success(f"{f}")
        else:
            print_error(f"{f} - MISSING")
            all_ok = False
    
    print("\nCore Package:")
    core_files = ['core/__init__.py', 'core/config.py', 'core/utils.py']
    for f in core_files:
        path = Path(f)
        if path.exists():
            print_success(f"{f}")
        else:
            print_error(f"{f} - MISSING")
            all_ok = False
    
    return all_ok

def count_templates():
    """Count available templates"""
    print_header("COUNTING TEMPLATES")
    
    templates_dir = Path('templates')
    if not templates_dir.exists():
        print_error("templates/ directory not found")
        return 0
    
    template_dirs = [d for d in templates_dir.iterdir() if d.is_dir()]
    count = len(template_dirs)
    
    print_info(f"Found {count} template directories")
    print(f"\nTemplates:")
    for i, d in enumerate(sorted(template_dirs), 1):
        print(f"  {i:2d}. {d.name}")
    
    return count

def show_usage():
    """Show usage instructions"""
    print_header("QUICK START GUIDE")
    
    print("1. Install Dependencies:")
    print("   $ pip install -r requirements.txt\n")
    
    print("2. Configure Environment (optional):")
    print("   $ cp .env.example .env")
    print("   $ nano .env  # Edit settings\n")
    
    print("3. Run the Application:")
    print("   $ python3 socialhook-x.py\n")
    
    print("4. Follow the Interactive Menu:")
    print("   [1] Select Template")
    print("   [2] Configure Tunnel")
    print("   [3] Set Custom Port")
    print("   [4] View Captured Data")
    print("   [5] System Information\n")

def show_resources():
    """Show available resources"""
    print_header("RESOURCES & DOCUMENTATION")
    
    print("📖 Documentation:")
    print("   • README.md - Complete project documentation")
    print("   • .env.example - Configuration template")
    print("   • COMPLETION_SUMMARY.md - Project summary\n")
    
    print("🔧 Main Files:")
    print("   • socialhook-x.py - Main application")
    print("   • install-socialhook.py - Installer script")
    print("   • core/config.py - Configuration system")
    print("   • core/utils.py - Utility functions\n")
    
    print("📁 Data Directories:")
    print("   • templates/ - Phishing templates (44+)")
    print("   • captured_data/ - Captured credentials")
    print("   • output/ - Output files (.txt)")
    print("   • servers/ - Active server instances\n")

def main():
    """Main entry point"""
    print_header("SocialHook-X v4.0 Verification Tool")
    
    # Verify structure
    structure_ok = verify_structure()
    
    if not structure_ok:
        print_error("\nSome files or directories are missing!")
        return 1
    
    print_success("\n✓ Project structure verified!")
    
    # Count templates
    print()
    template_count = count_templates()
    print_success(f"\n✓ {template_count} templates available!")
    
    # Show usage
    print()
    show_usage()
    
    # Show resources
    show_resources()
    
    print_header("SETUP COMPLETE!")
    print("Ready to start SocialHook-X v4.0!")
    print("\n📝 Remember:")
    print("   ✓ Get proper authorization before testing")
    print("   ✓ Use ethically and legally")
    print("   ✓ Protect captured data")
    print("   ✓ Follow all security best practices\n")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)
