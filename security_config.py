#!/usr/bin/env python3
"""
Security configuration for the SRU Cyberspace Club website.
Contains additional security settings and monitoring capabilities.
"""

import os
import logging
from datetime import datetime, timedelta

# Security Configuration
SECURITY_CONFIG = {
    # Session Security
    'SESSION_TIMEOUT': 3600,  # 1 hour
    'SESSION_RENEWAL': True,
    'MAX_SESSIONS_PER_IP': 5,
    
    # Rate Limiting
    'RATE_LIMIT_DEFAULT': "200 per day, 50 per hour",
    'RATE_LIMIT_LOGIN': "5 per minute",
    'RATE_LIMIT_FORM': "10 per minute",
    'RATE_LIMIT_API': "100 per hour",
    
    # Input Validation
    'MAX_INPUT_LENGTH': 1000,
    'ALLOWED_FILE_TYPES': ['.txt', '.pdf', '.doc', '.docx'],
    'MAX_FILE_SIZE': 16 * 1024 * 1024,  # 16MB
    
    # IP Blocking
    'AUTO_BLOCK_SUSPICIOUS': True,
    'BLOCK_DURATION': 3600,  # 1 hour
    'MAX_FAILED_ATTEMPTS': 5,
    
    # Logging
    'LOG_LEVEL': 'INFO',
    'LOG_FILE': 'security.log',
    'LOG_MAX_SIZE': 10 * 1024 * 1024,  # 10MB
    'LOG_BACKUP_COUNT': 5,
    
    # Content Security Policy
    'CSP_REPORT_ONLY': False,
    'CSP_REPORT_URI': None,
    
    # Headers
    'STRICT_TRANSPORT_SECURITY': True,
    'HSTS_MAX_AGE': 31536000,  # 1 year
    'HSTS_INCLUDE_SUBDOMAINS': True,
    'HSTS_PRELOAD': True,
}

# Suspicious Patterns
SUSPICIOUS_PATTERNS = [
    # XSS Patterns
    r'<script[^>]*>.*?</script>',
    r'javascript:',
    r'vbscript:',
    r'data:',
    r'on\w+\s*=',
    r'<iframe[^>]*>',
    r'<object[^>]*>',
    r'<embed[^>]*>',
    
    # SQL Injection Patterns
    r'(\b(union|select|insert|update|delete|drop|create|alter|exec|execute)\b)',
    r'(\b(or|and)\b\s+\d+\s*=\s*\d+)',
    r'(\b(union|select)\b\s+.*\bfrom\b)',
    
    # Command Injection
    r'(\b(cmd|command|exec|system|eval|execfile|input|raw_input)\b)',
    r'(\b(rm|del|format|fdisk|mkfs|dd|wget|curl|nc|netcat)\b)',
    
    # Path Traversal
    r'\.\./',
    r'\.\.\\',
    r'%2e%2e%2f',
    r'%2e%2e%5c',
    
    # File Inclusion
    r'(\b(include|require|include_once|require_once)\b\s*[\'"][^\'"]*\.\.)',
    
    # LDAP Injection
    r'(\b(ldap|ldaps)\b\s*[\'"][^\'"]*[()])',
    
    # NoSQL Injection
    r'(\b(\$where|\$ne|\$gt|\$lt|\$regex)\b)',
]

# Allowed Domains for External Resources
ALLOWED_DOMAINS = {
    'fonts': ['fonts.googleapis.com', 'fonts.gstatic.com'],
    'cdn': ['cdnjs.cloudflare.com', 'cdn.jsdelivr.net'],
    'calendar': ['calendar.google.com'],
    'analytics': [],  # Add if needed
}

# Security Headers Configuration
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
    'Cross-Origin-Embedder-Policy': 'require-corp',
    'Cross-Origin-Opener-Policy': 'same-origin',
    'Cross-Origin-Resource-Policy': 'same-origin',
}

# Content Security Policy
CSP_POLICY = {
    'default-src': ["'self'"],
    'script-src': ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com"],
    'style-src': ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com"],
    'font-src': ["'self'", "https://cdnjs.cloudflare.com", "https://fonts.gstatic.com"],
    'img-src': ["'self'", "data:", "https:"],
    'connect-src': ["'self'"],
    'frame-src': ["'self'", "https://calendar.google.com"],
    'object-src': ["'none'"],
    'base-uri': ["'self'"],
    'form-action': ["'self'"],
    'frame-ancestors': ["'none'"],
    'upgrade-insecure-requests': True,
}

# Logging Configuration
def setup_security_logging():
    """Setup security logging with rotation"""
    from logging.handlers import RotatingFileHandler
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Security logger
    security_logger = logging.getLogger('security')
    security_logger.setLevel(logging.INFO)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        'logs/security.log',
        maxBytes=SECURITY_CONFIG['LOG_MAX_SIZE'],
        backupCount=SECURITY_CONFIG['LOG_BACKUP_COUNT']
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    security_logger.addHandler(file_handler)
    security_logger.addHandler(console_handler)
    
    return security_logger

# Security Monitoring
class SecurityMonitor:
    def __init__(self):
        self.logger = setup_security_logging()
        self.attack_attempts = {}
        self.blocked_ips = set()
        self.suspicious_activity = []
    
    def log_attack_attempt(self, ip_address, attack_type, details):
        """Log attack attempts for monitoring"""
        timestamp = datetime.now()
        
        if ip_address not in self.attack_attempts:
            self.attack_attempts[ip_address] = []
        
        self.attack_attempts[ip_address].append({
            'timestamp': timestamp,
            'type': attack_type,
            'details': details
        })
        
        # Log the attempt
        self.logger.warning(
            f"Attack attempt detected - IP: {ip_address}, "
            f"Type: {attack_type}, Details: {details}"
        )
        
        # Check if IP should be blocked
        recent_attempts = [
            attempt for attempt in self.attack_attempts[ip_address]
            if timestamp - attempt['timestamp'] < timedelta(hours=1)
        ]
        
        if len(recent_attempts) >= SECURITY_CONFIG['MAX_FAILED_ATTEMPTS']:
            self.block_ip(ip_address, "Multiple attack attempts")
    
    def block_ip(self, ip_address, reason):
        """Block an IP address"""
        self.blocked_ips.add(ip_address)
        self.logger.warning(f"IP {ip_address} blocked: {reason}")
    
    def unblock_ip(self, ip_address):
        """Unblock an IP address"""
        if ip_address in self.blocked_ips:
            self.blocked_ips.remove(ip_address)
            self.logger.info(f"IP {ip_address} unblocked")
    
    def get_security_report(self):
        """Generate security report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'blocked_ips_count': len(self.blocked_ips),
            'attack_attempts_count': sum(len(attempts) for attempts in self.attack_attempts.values()),
            'recent_suspicious_activity': self.suspicious_activity[-10:],
            'blocked_ips': list(self.blocked_ips)
        }

# Initialize security monitor
security_monitor = SecurityMonitor()

