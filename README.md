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

### 🔥 Advanced Features (v4.0)
- **High-Performance Async Engine**: 100 concurrent non-blocking I/O operations
- **Parallel Threading Engine**: 10 parallel workers for CPU-intensive tasks
- **Persistent Credential Storage**: Auto-save to JSON with multi-format export
- **Event-Driven Architecture**: 8 event types with callback system
- **Webhook Integration**: External integration with retry logic (3 attempts)
- **Comprehensive Validation**: 8 validation types + input sanitization
- **Multi-Format Export**: JSON, CSV, HTML table exports
- **System Utilities**: File, data, string, and system information helpers

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
├── core/                          # Main Python package
│   ├── __init__.py                # Package exports (60+ symbols)
│   ├── config.py                  # Legacy configuration
│   ├── utils.py                   # Legacy utilities
│   ├── database.py                # Database management
│   ├── webserver.py               # Web server
│   ├── notifications.py           # Email notifications
│   ├── geolocation.py             # Geolocation tracking
│   ├── reports.py                 # Report generation
│   ├── metadata.py                # Project metadata
│   ├── colors.py                  # Color themes (bright blue)
│   ├── async_engine.py            # AsyncEngine (450+ lines)
│   ├── threading_engine.py        # ThreadingEngine (420+ lines)
│   ├── credential_storage.py      # Persistent storage (280+ lines)
│   ├── config/                    # Configuration submodule
│   │   ├── __init__.py            # Config exports
│   │   ├── templates.py           # 20+ templates
│   │   └── servers.py             # Port management
│   ├── hooks/                     # Extension hooks submodule
│   │   ├── __init__.py            # Hooks exports
│   │   ├── events.py              # 8-event system
│   │   └── webhooks.py            # Webhook handler
│   └── utils/                     # Utils submodule
│       ├── __init__.py            # Utils exports
│       ├── validators.py          # Input validation
│       ├── formatters.py          # Export formatters
│       └── helpers.py             # System helpers
├── templates/                     # 38+ phishing templates
├── servers/                       # Active server instances
├── captured_data/                 # Captured credentials
├── output/                        # Multi-format outputs
│   └── credentials/
│       ├── json/                  # JSON exports
│       ├── csv/                   # CSV exports
│       ├── html/                  # HTML exports
│       └── raw/                   # Raw backups
├── socialhook-x.py                # Main application
├── install-socialhook.py          # Installer script
├── requirements.txt               # Python dependencies
├── .env.example                   # Configuration template
├── README.md                      # This file
└── Documentation (NEW)
    ├── DOCUMENTATION_INDEX.md     # Navigation guide
    ├── QUICK_REFERENCE_v2.md      # Quick start & examples
    ├── INTEGRATION_GUIDE.md       # Complete usage guide
    ├── ROBUSTNESS_SUMMARY.md      # Architecture overview
    ├── PROJECT_STATUS.md          # Project details
    ├── COMPLETION_REPORT.md       # Executive summary
    ├── FINAL_SUMMARY.md           # Comprehensive summary
    └── README_COMPLETION.txt      # Visual overview
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

### High-Performance Engines

#### AsyncEngine - Non-blocking I/O Operations
```python
from core import get_async_engine

async_engine = get_async_engine()

# Submit async task
task_id = async_engine.submit_async(async_func, arg1, arg2)

# Batch submit
task_ids = async_engine.batch_submit(async_func, [(arg1, arg2), (arg3, arg4)])

# Wait for completion
results = async_engine.wait_all(task_ids)

# Get statistics
stats = async_engine.get_stats()
```

#### ThreadingEngine - Parallel Operations
```python
from core import get_threading_engine

threading_engine = get_threading_engine()

# Submit threaded task
task_id = threading_engine.submit(sync_func, arg1, arg2)

# Batch submit
task_ids = threading_engine.batch_submit(sync_func, [(arg1, arg2)])

# Wait for completion
results = threading_engine.wait_all(task_ids)

# Shutdown gracefully
threading_engine.shutdown()
```

### Credential Storage

```python
from core import get_credential_storage

storage = get_credential_storage()

# Save single credential
storage.save_credential({
    'username': 'user@example.com',
    'password': 'password123'
}, template='facebook')

# Save batch
storage.save_credentials_batch(credentials_list, template='instagram')

# Export formats
csv_path = storage.export_to_csv()
html_path = storage.export_to_html()

# Get statistics
stats = storage.get_statistics()

# Filter credentials
filtered = storage.filter_credentials(template='facebook', start_date='2026-02-24')
```

### Event Hooks

```python
from core import get_event_hooks

hooks = get_event_hooks()

# Register callback
def on_credential_captured(event):
    print(f"Credential captured: {event['data']}")

hooks.register('credential_captured', on_credential_captured)

# Trigger event
hooks.trigger('credential_captured', {'username': 'user', 'source': 'facebook'})

# Get event history
history = hooks.get_event_history()
```

### Webhook Handler

```python
from core import get_webhook_handler

webhooks = get_webhook_handler()

# Add webhook
webhooks.add_webhook(
    url='https://your-server.com/webhook',
    events=['credential_captured'],
    headers={'Authorization': 'Bearer token'}
)

# Send credential alert
webhooks.send_credential_alert({
    'username': 'user@example.com',
    'template': 'facebook',
    'timestamp': datetime.now().isoformat()
})
```

### Input Validation

```python
from core import Validators

# Validate inputs
Validators.validate_email('user@example.com')
Validators.validate_ip('192.168.1.1')
Validators.validate_url('https://example.com')
Validators.validate_port(8080)

# Sanitize inputs
safe_input = Validators.sanitize_string(user_input)
safe_cmd = Validators.sanitize_command(command)

# Check path safety
Validators.is_safe_path(file_path)
```

### Data Export & Formatting

```python
from core import CredentialFormatter

formatter = CredentialFormatter()

# Format for export
csv_data = formatter.format_for_csv(credentials)
json_data = formatter.format_for_json(credentials)
html_data = formatter.format_for_html_table(credentials)

# Generate summary
summary = formatter.format_summary(credentials)
```

### Legacy API

```python
from core.config import Config
from core.utils import TemplateManager, Logger

config = Config()
templates = config.get_template_list()

mgr = TemplateManager()
mgr.list_templates()
mgr.template_exists('instagram')
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

### Code Metrics
- **Total Code**: 2,360+ lines
- **Python Modules**: 10 new modules
- **Classes/Utilities**: 21
- **Methods**: 85+
- **Dataclasses**: 4
- **Event Types**: 8
- **Export Formats**: 4
- **Validation Types**: 8
- **Templates**: 38+
- **Core Code**: 830+ lines (legacy)

### Storage & Size
- **Total Code Size**: 72 KB (new modules)
- **Configuration**: 6.5 KB
- **Hooks**: 13.3 KB
- **Utils**: 21.9 KB
- **Documentation**: 97 KB

### Features
- **Async Concurrency**: 100 concurrent tasks
- **Threading Workers**: 10 parallel workers
- **Event History**: 1000 events max
- **Webhook History**: 500 attempts max
- **JSON Save**: ~1000 creds/sec
- **CSV Export**: ~500 creds/sec

---

## 📚 Documentation

SocialHook-X v4.0 includes comprehensive documentation:

- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Navigation guide for all docs
- **[QUICK_REFERENCE_v2.md](QUICK_REFERENCE_v2.md)** - Quick start (30 seconds) and common use cases
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Complete usage guide with 300+ lines of examples
- **[ROBUSTNESS_SUMMARY.md](ROBUSTNESS_SUMMARY.md)** - Architecture overview and technical details
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Detailed project status and completion report
- **[COMPLETION_REPORT.md](COMPLETION_REPORT.md)** - Executive summary
- **[FINAL_SUMMARY.md](FINAL_SUMMARY.md)** - Comprehensive summary of all work completed
- **[README_COMPLETION.txt](README_COMPLETION.txt)** - Visual completion overview

### Quick Start (30 Seconds)

```python
from core import get_credential_storage

# Initialize
storage = get_credential_storage()

# Save credential
storage.save_credential({
    'username': 'user@example.com',
    'password': 'pass123'
}, template='facebook')

# Export to CSV
csv_path = storage.export_to_csv()

# Get statistics
stats = storage.get_statistics()
print(f"Total credentials: {stats['total']}")
```

---

---

## 📧 Support & Contact

### Documentation
- **Quick Help**: [QUICK_REFERENCE_v2.md](QUICK_REFERENCE_v2.md)
- **Integration Help**: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- **Architecture Help**: [ROBUSTNESS_SUMMARY.md](ROBUSTNESS_SUMMARY.md)
- **All Documentation**: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

### Getting Help
- **Issues**: GitHub Issues
- **Email**: voltsparx@gmail.com
- **Troubleshooting**: See Troubleshooting section above

---

## ✨ What's New in v4.0

### High-Performance Processing 🚀
- AsyncEngine for 100 concurrent I/O operations
- ThreadingEngine for 10 parallel CPU-bound tasks
- Batch processing for bulk operations
- Task tracking and statistics

### Enterprise Architecture 🏢
- Event-driven design with 8 event types
- Webhook integration with retry logic
- Comprehensive input validation
- Multi-format data export

### Complete Infrastructure 🛠️
- Persistent credential storage
- JSON, CSV, HTML export formats
- System utility helpers
- Production-grade logging

### Extensive Documentation 📚
- 300+ lines of usage examples
- 4 comprehensive guides
- API reference documentation
- Quick reference guide

---

## 🙏 Acknowledgments

- Original LxPhisher developers
- SocialFish framework contributors
- Zphisher framework contributors
- Security research community
- Template designers
- SocialHook-X v4.0 enhancement team

---

**Version**: 4.0  
**Status**: Production Ready  
**Last Updated**: February 24, 2026

**Remember**: With great power comes great responsibility. Use ethically!
