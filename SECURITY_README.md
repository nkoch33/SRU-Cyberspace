# SRU Cyberspace Club Website Security Implementation

## Overview
This document outlines the comprehensive security measures implemented to protect the SRU Cyberspace Club website from malicious attacks, ensuring a safe environment for all students.

## Quick Start

### Running the Secure Server
```bash
# Install dependencies
pip install -r requirements.txt

# Start the secure server
python secure_server.py

# Or use the original simple server
python server.py
```

## Security Features Implemented

### 1. **Input Validation & Sanitization**
- **XSS Prevention**: All user inputs are sanitized to remove malicious scripts
- **HTML Encoding**: Dangerous characters are automatically escaped
- **Pattern Detection**: Blocks common attack patterns in real-time
- **Length Validation**: Prevents buffer overflow attacks

### 2. **CSRF (Cross-Site Request Forgery) Protection**
- **Token Generation**: Unique CSRF tokens for each session
- **Form Validation**: All forms require valid CSRF tokens
- **Automatic Expiration**: Tokens expire after 1 hour
- **Session Management**: Secure session handling

### 3. **Rate Limiting**
- **Request Limits**: 
  - General: 200 requests per day, 50 per hour
  - Forms: 10 submissions per minute
  - API: 100 requests per hour
- **IP-based Tracking**: Prevents abuse from single sources
- **Automatic Blocking**: Suspicious IPs are temporarily blocked

### 4. **Security Headers**
- **X-Content-Type-Options**: Prevents MIME type sniffing
- **X-Frame-Options**: Blocks clickjacking attacks
- **X-XSS-Protection**: Additional XSS protection
- **Referrer-Policy**: Controls referrer information
- **Permissions-Policy**: Restricts browser features

### 5. **Content Security Policy (CSP)**
- **Script Sources**: Only allows trusted domains
- **Style Sources**: Restricts CSS sources
- **Frame Sources**: Limits iframe sources to Google Calendar
- **Object Sources**: Blocks dangerous object types

### 6. **Session Security**
- **Secure Cookies**: HTTPS-only cookie transmission
- **HttpOnly**: Prevents JavaScript access to cookies
- **SameSite**: Protects against CSRF attacks
- **Automatic Expiration**: Sessions timeout after 1 hour

### 7. **Attack Detection & Prevention**
- **Pattern Recognition**: Detects common attack signatures
- **IP Blocking**: Automatically blocks malicious IPs
- **Real-time Monitoring**: Logs all suspicious activity
- **Threat Response**: Immediate response to detected threats

## File Structure

```
SRU CYBERSPACE/
├── secure_server.py      # Secure Flask server
├── server.py            # Simple HTTP server
├── security.py          # Core security module
├── security_config.py   # Security configuration
├── requirements.txt     # Python dependencies
├── index.html          # Main website
├── styles.css          # Styling
├── script.js           # Client-side JavaScript
└── logs/               # Security logs directory
```

## Configuration

### Environment Variables
```bash
# Set a strong secret key
export SECRET_KEY="your-super-secret-key-here"

# Set custom port
export PORT=8000
```

### Security Settings
All security settings can be modified in `security_config.py`:

```python
SECURITY_CONFIG = {
    'SESSION_TIMEOUT': 3600,        # Session timeout in seconds
    'MAX_FAILED_ATTEMPTS': 5,       # Max attempts before IP blocking
    'BLOCK_DURATION': 3600,         # IP block duration in seconds
    'RATE_LIMIT_DEFAULT': "200 per day, 50 per hour"
}
```

## Monitoring & Logging

### Security Logs
- **Location**: `logs/security.log`
- **Rotation**: Automatic rotation at 10MB
- **Retention**: Keeps 5 backup files
- **Format**: Structured logging with timestamps

### Log Examples
```
2024-01-15 10:30:15 - security - WARNING - Attack attempt detected - IP: 192.168.1.100, Type: XSS, Details: <script>alert('xss')</script>
2024-01-15 10:30:16 - security - WARNING - IP 192.168.1.100 blocked: Multiple attack attempts
2024-01-15 10:30:20 - security - INFO - Form submitted successfully - Name: John Doe, Email: john@example.com
```

### Security Reports
Access security status via the monitoring API:
```python
from security_config import security_monitor

# Get current security status
report = security_monitor.get_security_report()
print(f"Blocked IPs: {report['blocked_ips_count']}")
print(f"Attack attempts: {report['attack_attempts_count']}")
```

## Threat Response

### Automatic Responses
1. **Suspicious Input**: Immediate rejection with logging
2. **Rate Limit Exceeded**: Temporary blocking (429 response)
3. **Multiple Attacks**: IP address blocking for 1 hour
4. **CSRF Violation**: Form rejection with security logging

### Manual Actions
```python
from security_config import security_monitor

# Block an IP manually
security_monitor.block_ip("192.168.1.100", "Manual block")

# Unblock an IP
security_monitor.unblock_ip("192.168.1.100")

# View blocked IPs
blocked_ips = security_monitor.blocked_ips
```

## Testing Security

### Test Cases
1. **XSS Injection**: Try `<script>alert('xss')</script>`
2. **SQL Injection**: Try `' OR 1=1 --`
3. **CSRF Attack**: Submit form without valid token
4. **Rate Limiting**: Send multiple rapid requests
5. **File Upload**: Try uploading executable files

### Expected Results
- All malicious inputs should be rejected
- Attack attempts should be logged
- IPs should be blocked after multiple violations
- Forms should require valid CSRF tokens

## Deployment Security

### Production Checklist
- [ ] Set strong `SECRET_KEY` environment variable
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerting
- [ ] Regular security updates
- [ ] Backup security logs

### Server Hardening
```bash
# Update system packages
sudo apt update && sudo apt upgrade

# Configure firewall
sudo ufw enable
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Set up fail2ban (optional)
sudo apt install fail2ban
```

## Security Best Practices

### For Developers
1. **Never trust user input**
2. **Always validate and sanitize data**
3. **Use HTTPS in production**
4. **Keep dependencies updated**
5. **Monitor security logs regularly**

### For Administrators
1. **Regular security audits**
2. **Monitor attack patterns**
3. **Update security configurations**
4. **Train users on security**
5. **Have incident response plan**

## Emergency Response

### If Under Attack
1. **Immediate Actions**:
   - Check security logs
   - Identify attack patterns
   - Block malicious IPs
   - Notify security team

2. **Recovery Steps**:
   - Analyze attack vectors
   - Update security rules
   - Restore from clean backups
   - Document incident

3. **Post-Incident**:
   - Review security measures
   - Update threat models
   - Improve monitoring
   - Conduct lessons learned

## Support & Resources

### Security Contacts
- **Security Issues**: Report to IT security team
- **Technical Support**: Contact system administrator
- **Emergency**: Follow incident response procedures

### Additional Resources
- [OWASP Security Guidelines](https://owasp.org/)
- [Flask Security Documentation](https://flask-security.readthedocs.io/)
- [Python Security Best Practices](https://python-security.readthedocs.io/)

---

**Remember**: Security is an ongoing process. Regularly review and update these measures to stay protected against evolving threats.

**Last Updated**: January 2024
**Version**: 1.0
**Maintainer**: SRU Cyberspace Club IT Team
