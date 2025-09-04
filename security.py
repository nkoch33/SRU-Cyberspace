import re
import hashlib
import secrets
import time
from urllib.parse import urlparse
import html

class SecurityManager:
    def __init__(self):
        self.csrf_tokens = {}
        self.rate_limit_data = {}
        self.blocked_ips = set()
        
    def sanitize_input(self, user_input):
        """Sanitize user input to prevent XSS and injection attacks"""
        if not user_input:
            return ""
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', 'javascript:', 'vbscript:', 'onload', 'onerror']
        sanitized = str(user_input)
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        # HTML encode remaining content
        sanitized = html.escape(sanitized)
        
        # Remove script tags and event handlers
        script_pattern = r'<script[^>]*>.*?</script>'
        event_pattern = r'on\w+\s*='
        
        sanitized = re.sub(script_pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(event_pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()
    
    def validate_email(self, email):
        """Validate email format and prevent email injection"""
        if not email:
            return False
        
        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'javascript:',
            r'vbscript:',
            r'data:',
            r'<script',
            r'javascript\(',
            r'vbscript\('
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, email, re.IGNORECASE):
                return False
        
        return True
    
    def validate_name(self, name):
        """Validate name input"""
        if not name:
            return False
        
        # Only allow letters, spaces, hyphens, and apostrophes
        name_pattern = r'^[a-zA-Z\s\'-]+$'
        if not re.match(name_pattern, name):
            return False
        
        # Length validation
        if len(name) < 2 or len(name) > 50:
            return False
        
        return True
    
    def generate_csrf_token(self, session_id):
        """Generate CSRF token for form protection"""
        token = secrets.token_urlsafe(32)
        self.csrf_tokens[session_id] = {
            'token': token,
            'timestamp': time.time()
        }
        return token
    
    def validate_csrf_token(self, session_id, token):
        """Validate CSRF token"""
        if session_id not in self.csrf_tokens:
            return False
        
        stored_data = self.csrf_tokens[session_id]
        
        # Check if token matches
        if stored_data['token'] != token:
            return False
        
        # Check if token is expired (1 hour)
        if time.time() - stored_data['timestamp'] > 3600:
            del self.csrf_tokens[session_id]
            return False
        
        return True
    
    def rate_limit(self, ip_address, limit=10, window=60):
        """Implement rate limiting to prevent abuse"""
        current_time = time.time()
        
        if ip_address not in self.rate_limit_data:
            self.rate_limit_data[ip_address] = []
        
        # Clean old requests
        self.rate_limit_data[ip_address] = [
            req_time for req_time in self.rate_limit_data[ip_address]
            if current_time - req_time < window
        ]
        
        # Check if limit exceeded
        if len(self.rate_limit_data[ip_address]) >= limit:
            return False
        
        # Add current request
        self.rate_limit_data[ip_address].append(current_time)
        return True
    
    def is_suspicious_request(self, request_data):
        """Detect suspicious request patterns"""
        suspicious_patterns = [
            r'<script',
            r'javascript:',
            r'vbscript:',
            r'data:',
            r'<iframe',
            r'<object',
            r'<embed',
            r'<form',
            r'<input',
            r'<textarea',
            r'<select',
            r'<button',
            r'<link',
            r'<meta',
            r'<style',
            r'<base',
            r'<bgsound',
            r'<link',
            r'<meta',
            r'<title',
            r'<xmp',
            r'<plaintext',
            r'<listing',
            r'<marquee',
            r'<applet',
            r'<param',
            r'<embed',
            r'<object',
            r'<basefont',
            r'<isindex',
            r'<dir',
            r'<menu',
            r'<listing',
            r'<plaintext',
            r'<xmp',
            r'<nextid',
            r'<comment',
            r'<listing',
            r'<plaintext',
            r'<xmp',
            r'<nextid',
            r'<comment',
            r'<listing',
            r'<plaintext',
            r'<xmp',
            r'<nextid',
            r'<comment'
        ]
        
        request_str = str(request_data).lower()
        
        for pattern in suspicious_patterns:
            if re.search(pattern, request_str, re.IGNORECASE):
                return True
        
        return False
    
    def validate_url(self, url):
        """Validate URL to prevent open redirect attacks"""
        if not url:
            return False
        
        try:
            parsed = urlparse(url)
            
            # Only allow HTTP and HTTPS
            if parsed.scheme not in ['http', 'https']:
                return False
            
            # Block localhost and private IPs
            if parsed.hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
                return False
            
            # Block private IP ranges
            if parsed.hostname and self.is_private_ip(parsed.hostname):
                return False
            
            return True
        except:
            return False
    
    def is_private_ip(self, hostname):
        """Check if hostname resolves to private IP"""
        try:
            import socket
            ip = socket.gethostbyname(hostname)
            
            # Private IP ranges
            private_ranges = [
                ('10.0.0.0', '10.255.255.255'),
                ('172.16.0.0', '172.31.255.255'),
                ('192.168.0.0', '192.168.255.255')
            ]
            
            for start, end in private_ranges:
                if self.ip_in_range(ip, start, end):
                    return True
            
            return False
        except:
            return False
    
    def ip_in_range(self, ip, start, end):
        """Check if IP is in range"""
        try:
            ip_int = int(''.join([f'{int(x):08b}' for x in ip.split('.')]), 2)
            start_int = int(''.join([f'{int(x):08b}' for x in start.split('.')]), 2)
            end_int = int(''.join([f'{int(x):08b}' for x in end.split('.')]), 2)
            return start_int <= ip_int <= end_int
        except:
            return False
    
    def clean_session_data(self):
        """Clean expired session data"""
        current_time = time.time()
        
        # Clean expired CSRF tokens
        expired_sessions = [
            session_id for session_id, data in self.csrf_tokens.items()
            if current_time - data['timestamp'] > 3600
        ]
        
        for session_id in expired_sessions:
            del self.csrf_tokens[session_id]
        
        # Clean old rate limit data
        for ip in list(self.rate_limit_data.keys()):
            self.rate_limit_data[ip] = [
                req_time for req_time in self.rate_limit_data[ip]
                if current_time - req_time < 300  # 5 minutes
            ]
            
            if not self.rate_limit_data[ip]:
                del self.rate_limit_data[ip]

# Global security manager instance
security_manager = SecurityManager()

