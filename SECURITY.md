# Security Guidelines for SocialHook-X

## Overview

SocialHook-X v4.0 has been hardened against several critical security vulnerabilities. This document outlines the security improvements and best practices for using this framework.

## Security Improvements (v4.0.1)

### 1. Input Validation & Sanitization ✅
- All user input is sanitized using `Validators.sanitize_string()`
- SQL injection protection through parameterized queries
- Maximum field length enforcement (256 characters default)

### 2. Rate Limiting ✅
- Endpoint rate limiting: 100 requests per 60 seconds per IP
- Prevents credential capture flooding
- Configurable via `RateLimiter` class

### 3. Authentication & Authorization ✅
- API key authentication on protected endpoints (`/api/stats`, `/api/credentials`)
- Set `SHX_API_KEY` environment variable to enable
- Add `X-API-Key` header to API requests

### 4. Data Caching with TTL ✅
- Geolocation cache entries expire after 24 hours (configurable)
- Prevents stale data from being served indefinitely

### 5. Webhook Payload Sanitization ✅
- Sensitive fields (password, token, secret, api_key) redacted in webhook payloads
- Webhooks now send `***REDACTED***` for sensitive data
- Prevents credential leakage to external integrations

### 6. Improved Error Handling ✅
- Generic error responses to prevent information disclosure
- Detailed errors only in server logs
- Proper HTTP status codes (429 for rate limit, 401 for auth failures, etc.)

### 7. Race Condition Fixes ✅
- Thread-safe access to task dictionaries via locks
- Prevents data corruption in async/threading engines
- Safe task status checks

### 8. Memory Leak Prevention ✅
- Webhook history limited to 500 entries
- Old entries automatically purged
- Prevents unbounded memory growth

### 9. Database Optimization ✅
- Indexes created on frequently queried columns (template, timestamp)
- Database initialization only on first run
- Reduced startup overhead

### 10. Encryption Ready ✅
- New `core/encryption.py` module provides credential encryption
- Supports key generation and derivation from passwords
- Can encrypt specific fields in credential data
- Future integration planned for at-rest encryption

## Security Best Practices

### Environment Variables
```bash
# Set these before running the application
export SHX_HOST="0.0.0.0"              # Binding address
export SHX_PORT="8080"                  # Server port
export SHX_DEBUG="False"                # Never enable in production
export SHX_API_KEY="your-secret-key"   # For API access
export SHX_SECRET_KEY="persistent-key" # For sessions
```

### Configuration
1. **Always use environment variables** for sensitive config
2. **Store `.encryption_key` securely** if using encryption
3. **Rotate API keys regularly**
4. **Use HTTPS** in production (reverse proxy recommended)

### API Access
```bash
# Protected API endpoints require authentication
curl -H "X-API-Key: your-secret-key" http://localhost:8080/api/stats
curl -H "X-API-Key: your-secret-key" http://localhost:8080/api/credentials
```

### Data Handling
1. **Never expose credentials in logs** - already sanitized
2. **Use CSV/HTML exports for reporting** instead of raw database access
3. **Implement field-level encryption** using `CredentialEncryption` for sensitive deployments
4. **Archive old data** - implement retention policies

### Deployment
1. **Use a reverse proxy** (nginx, Apache) for:
   - HTTPS/TLS termination
   - Additional rate limiting
   - Request validation
   - Static file serving

2. **Network isolation**:
   - Run on private network only
   - Use firewall rules to restrict access
   - Block direct internet access

3. **Monitoring & Logging**:
   - Enable comprehensive logging
   - Monitor rate limit triggers
   - Alert on API key failures

## Known Limitations

1. **Not Production-Grade Encryption**: Current implementation uses Fernet (symmetric) only
   - For sensitive deployments, implement additional key management
   - Consider integration with HSM (Hardware Security Module) for key storage

2. **No Built-in Audit Log**: Track all changes in application code
   - Recommended: Implement audit logging middleware

3. **Single Instance**: No built-in clustering/replication
   - Use external database for multi-instance deployments
   - Implement state sharing via Redis or similar

## Security Audit Checklist

- [ ] Environment variables configured
- [ ] API key set and strong
- [ ] Database backup strategy implemented
- [ ] HTTPS enabled (via reverse proxy)
- [ ] Rate limiting tested
- [ ] Firewall rules enforced
- [ ] Logging enabled and monitored
- [ ] Regular security updates applied
- [ ] Audit logs reviewed periodically
- [ ] Incident response plan documented

## Reporting Security Issues

If you discover a security vulnerability:
1. Do NOT post it publicly
2. Document the issue carefully
3. Provide proof of concept if possible
4. Contact the security team privately

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE Most Dangerous: https://cwe.mitre.org/top25/
- Flask Security: https://flask.palletsprojects.com/en/latest/
- SQLite Security: https://www.sqlite.org/security.html

## Version History

- **v4.0.1** - Security hardening release
  - Added input validation
  - Implemented rate limiting
  - Added API key authentication
  - Fixed race conditions
  - Added webhook payload sanitization
  - Improved error handling
  - Added encryption module
  - Cache TTL implementation

