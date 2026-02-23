# SocialHook-X v4.0

![Version](https://img.shields.io/badge/version-4.0-brightgreen.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-red.svg)

A comprehensive, modular phishing framework for security testing and research. SocialHook-X is designed to help security professionals test their organization's security awareness and vulnerability to social engineering attacks.

**⚠️ DISCLAIMER:** This tool is intended solely for authorized security testing and educational purposes. Unauthorized access to computer systems is illegal. Always obtain proper authorization before testing any system.

---

## 🚀 Features

### Core Capabilities
- **38+ Phishing Templates**: Pre-built templates for major social platforms and services
- **Multi-Platform Support**: Works on Linux, macOS, and Windows (with PHP)
- **Tunnel Services**: Multiple tunnel options for secure credential capture
- **Automated Credential Logging**: Captures and logs submitted credentials
- **Template Management**: Easy template selection and configuration
- **Custom Port Support**: Run on any available port (1-65535)
- **Real-time Monitoring**: Monitor captured credentials in real-time
- **Modular Architecture**: Clean, extensible Python framework

### Supported Platforms (38+)
- ✅ Facebook (Standard & Advanced)
- ✅ Instagram (Standard, Verify, Followers)
- ✅ Google (Standard & New)
- ✅ LinkedIn
- ✅ Twitter
- ✅ GitHub
- ✅ GitLab
- ✅ Microsoft (Office 365)
- ✅ Apple iCloud
- ✅ Amazon
- ✅ PayPal
- ✅ Adobe Creative Cloud
- ✅ Dropbox
- ✅ Netflix
- ✅ Spotify
- ✅ Discord
- ✅ Twitch
- ✅ Reddit
- ✅ Snapchat
- ✅ TikTok
- ✅ Telegram
- ✅ WhatsApp
- ✅ Signal
- ✅ Viber
- ✅ Slack
- ✅ Gmail
- ✅ Yahoo Mail
- ✅ Hotmail
- ✅ ProtonMail
- ✅ WordPress
- ✅ Shopify
- ✅ Pinterest
- ✅ Medium
- ✅ Quora
- ✅ Stack Overflow
- ✅ DeviantArt
- ✅ Bitbucket
- ✅ Yandex
- ✅ VKontakte (VK)

---

## 📋 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **PHP**: 7.2+ (for running phishing templates)
- **Operating System**: Linux, macOS, or Windows (with WSL/PHP)
- **RAM**: 512 MB minimum
- **Disk Space**: 500 MB for full installation with all templates

### Dependencies
All Python dependencies are listed in `requirements.txt` and are automatically installed during setup.

---

## 🔧 Installation

### Quick Start (Linux/macOS)

```bash
# Clone the repository
git clone https://github.com/yourusername/socialhook-x.git
cd socialhook-x

# Run the installer
python3 install-socialhook.py

# Install Python dependencies
pip install -r requirements.txt

# Make the main script executable
chmod +x socialhook-x.py

# Run the application
python3 socialhook-x.py
```

### Manual Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/socialhook-x.git
   cd socialhook-x
   ```

2. **Install system dependencies**
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip php php-curl curl wget
   ```
   
   **macOS (with Homebrew):**
   ```bash
   brew install python3 php
   ```

3. **Install Python packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env as needed
   ```

5. **Run the application**
   ```bash
   python3 socialhook-x.py
   ```

### Windows Setup

1. Install Python 3.8+ from [python.org](https://www.python.org)
2. Install PHP from [php.net](https://www.php.net) or use WSL
3. Clone the repository
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python socialhook-x.py`

---

## 📖 Usage Guide

### Main Menu

When you run SocialHook-X, you'll see the main menu:

```
════════════════════════════════════════════════════════════════
[+] SocialHook-X v4.0 - Social Engineering Testing Framework
════════════════════════════════════════════════════════════════

[1] Select Template
[2] Configure Tunnel
[3] Set Custom Port
[4] View Captured Data
[5] System Information
[0] Exit

Select option:
```

### Available Templates

The framework includes 38+ phishing templates organized by platform:

**Social Media:**
- Facebook, Facebook Advanced, Facebook Messenger, Facebook Security
- Instagram, Instagram Followers, Instagram Verify, IG Followers, IG Verify
- TikTok, Snapchat, Twitter, Reddit
- Discord, Twitch, Telegram, Signal, Viber, WhatsApp, Slack

**Email & Communication:**
- Gmail, Yahoo, Hotmail, ProtonMail
- LinkedIn, Badoo

**Tech Platforms:**
- GitHub, GitLab, Bitbucket
- Microsoft (Office 365), Apple, Amazon
- Google (Standard & New)

**Services & Platforms:**
- PayPal, Adobe, Dropbox, Netflix, Spotify
- WordPress, Shopify, Pinterest, Medium, Quora, Stack Overflow
- DeviantArt, PlayStation, Roblox, Xbox, Steam, Origin
- Yandex, VKontakte (VK)

### Tunnel Configuration

Select from 5 tunnel services:
1. **localhost** - Direct local access (testing only)
2. **Cloudflared** - Cloudflare Tunnel with custom domain
3. **LocalXpose** - Fast local tunnel solution
4. **Ngrok** - Popular tunneling service
5. **localhost.run** - Simple SSH-based tunneling

### Custom Features

- **Custom Port Setting** - Run on any port (1-65535)
- **Credential Monitoring** - Real-time capture and logging
- **Data Export** - Export to .txt format
- **System Information** - Display system and project details

---

## 🔐 Security Best Practices

### Authorization & Consent
- ✅ Obtain written authorization before testing
- ✅ Get explicit consent from participants
- ✅ Define clear scope and duration
- ✅ Have management approval

### Environment Setup
- ✅ Use isolated testing environments
- ✅ Use VPN if required
- ✅ Secure the server with HTTPS
- ✅ Enable comprehensive logging

### During Testing
- ✅ Monitor actively for issues
- ✅ Be ready to stop the test
- ✅ Document all activities
- ✅ Track all metrics

### Data Protection
- ✅ Encrypt captured credentials
- ✅ Minimize data retention
- ✅ Secure storage of credentials
- ✅ Delete data after testing

### After Testing
- ✅ Immediate cleanup of all data
- ✅ Stop all services
- ✅ Provide feedback to users
- ✅ Conduct security training

---

## 📁 Project Structure

```
socialhook-x/
├── core/                    # Main Python package
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── utils.py            # Utility functions
│   ├── config/             # Config submodule
│   │   └── __init__.py
│   ├── hooks/              # Extension hooks
│   │   └── __init__.py
│   └── utils/              # Utils submodule
│       └── __init__.py
├── templates/              # 38+ phishing templates
├── servers/                # Active server instances
├── captured_data/          # Captured credentials
├── output/                 # .txt output files
├── third_party/            # External frameworks
│   ├── SocialFish/
│   └── Zphisher/
├── socialhook-x.py        # Main application
├── install-socialhook.py  # Installer script
├── requirements.txt        # Python dependencies
├── .env.example           # Configuration template
└── README.md              # This file
```

---

## ⚙️ Configuration

### .env Configuration

Copy `.env.example` to `.env`:

```bash
# Environment type
SHX_ENV=development

# Server configuration
SHX_HOST=127.0.0.1
SHX_PORT=8080

# Security settings
SHX_DEBUG=False
SHX_LOG_LEVEL=INFO

# Tunnel settings
SHX_DEFAULT_TUNNEL=localhost
SHX_TUNNEL_TIMEOUT=30
```

### Core Configuration

The `core/config.py` file contains:
- Path management (BASE_DIR, TEMPLATES_DIR, OUTPUT_DIR, etc.)
- 38+ template definitions
- Tunnel service configurations
- Environment-based settings

---

## 🛠️ API Reference

### Main Application

```python
from socialhook_x import SocialHookX

app = SocialHookX()
app.run()
```

### Configuration

```python
from core.config import Config

config = Config()
templates = config.get_template_list()
config.validate_template('facebook')
```

### Template Management

```python
from core.utils import TemplateManager

mgr = TemplateManager()
mgr.list_templates()
mgr.template_exists('instagram')
```

### Utilities

```python
from core.utils import (
    print_success, print_error, save_to_output,
    command_exists, run_command, get_timestamp
)
```

---

## 🐛 Troubleshooting

### PHP Not Found
```bash
# Ubuntu/Debian
sudo apt-get install php php-curl

# macOS
brew install php
```

### Port Already in Use
```bash
# Find process
lsof -i :8080

# Kill process
kill -9 <PID>
```

### Templates Not Loading
1. Check templates/ directory exists
2. Verify folder names match config
3. Ensure index.php exists
4. Fix permissions: `chmod -R 755 templates/`

### Python Module Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Run from project root
cd /path/to/socialhook-x
```

---

## 📝 Legal Disclaimer

**⚠️ WARNING: LEGAL IMPLICATIONS**

This tool is provided exclusively for:
- ✅ Authorized security testing
- ✅ Educational purposes
- ✅ Defensive security training
- ✅ Approved phishing simulations

**UNAUTHORIZED USE IS ILLEGAL:**
- ❌ Violates Computer Fraud and Abuse Act (CFAA)
- ❌ Violates similar laws worldwide
- ❌ Subject to criminal and civil penalties
- ❌ Can result in imprisonment

**Users are solely responsible for:**
- Obtaining proper authorization
- Ensuring legal compliance
- Using ethically and responsibly
- All consequences of misuse

---

## 🤝 Contributing

Contributions welcome! Process:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

### Adding New Templates
1. Create directory: `templates/platform/`
2. Add index.php, login.html, login.php
3. Register in core/config.py
4. Test thoroughly

---

## 📊 Project Statistics

- **Total Templates**: 38+
- **Supported Platforms**: 38 major services
- **Core Code**: 830+ lines
- **Configuration Options**: 25+
- **Python Version**: 3.8+
- **Dependencies**: 10+

---

## 📧 Support & Contact

- **Issues**: GitHub Issues
- **Email**: voltsparx@gmail.com
- **Troubleshooting**: See Troubleshooting section above

---

## 🙏 Acknowledgments

- Original LxPhisher developers
- SocialFish framework contributors
- Zphisher framework contributors
- Security research community
- Template designers

---

**Version**: 4.0  
**Status**: Active Development  
**Last Updated**: 2024

**Remember**: With great power comes great responsibility. Use ethically!
