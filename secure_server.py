#!/usr/bin/env python3
"""
Secure Flask server for the SRU Cyberspace Club website.
Implements comprehensive security measures to protect against malicious attacks.
"""

from flask import Flask, render_template, request, jsonify, session, make_response, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import uuid
import time
import logging
from pathlib import Path
from security import security_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(32))

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Security configuration
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=3600,  # 1 hour
    MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16MB max file size
)

@app.before_request
def security_checks():
    """Perform security checks before each request"""
    try:
        # Get client IP
        client_ip = request.remote_addr
        
        # Check if IP is blocked
        if client_ip in security_manager.blocked_ips:
            logger.warning(f"Blocked request from blocked IP: {client_ip}")
            abort(403)
        
        # Rate limiting check
        if not security_manager.rate_limit(client_ip, limit=20, window=60):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            abort(429)
        
        # Check for suspicious request patterns
        if security_manager.is_suspicious_request(request):
            logger.warning(f"Suspicious request detected from IP: {client_ip}")
            security_manager.blocked_ips.add(client_ip)
            abort(400)
        
        # Generate session ID if not exists
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        # Clean expired session data periodically
        if time.time() % 300 < 1:  # Every 5 minutes
            security_manager.clean_session_data()
            
    except Exception as e:
        logger.error(f"Security check error: {e}")
        abort(500)

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    # Content Security Policy
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
        "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
        "font-src 'self' https://cdnjs.cloudflare.com https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self'; "
        "frame-src 'self' https://calendar.google.com; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none';"
    )
    response.headers['Content-Security-Policy'] = csp
    
    return response

@app.route('/')
def index():
    """Serve the main page"""
    try:
        # Generate CSRF token for forms
        csrf_token = security_manager.generate_csrf_token(session['session_id'])
        
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Inject CSRF token into forms
        content = content.replace('</form>', f'<input type="hidden" name="csrf_token" value="{csrf_token}"></form>')
        
        response = make_response(content)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
        
    except Exception as e:
        logger.error(f"Error serving index: {e}")
        abort(500)

@app.route('/styles.css')
def styles():
    """Serve CSS file"""
    try:
        with open('styles.css', 'r', encoding='utf-8') as f:
            content = f.read()
        
        response = make_response(content)
        response.headers['Content-Type'] = 'text/css; charset=utf-8'
        return response
        
    except Exception as e:
        logger.error(f"Error serving CSS: {e}")
        abort(500)

@app.route('/script.js')
def script():
    """Serve JavaScript file"""
    try:
        with open('script.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        response = make_response(content)
        response.headers['Content-Type'] = 'application/javascript; charset=utf-8'
        return response
        
    except Exception as e:
        logger.error(f"Error serving JavaScript: {e}")
        abort(500)

@app.route('/submit-form', methods=['POST'])
@limiter.limit("5 per minute")
def submit_form():
    """Handle form submission with security validation"""
    try:
        # Validate CSRF token
        csrf_token = request.form.get('csrf_token')
        if not security_manager.validate_csrf_token(session['session_id'], csrf_token):
            logger.warning(f"CSRF token validation failed for IP: {request.remote_addr}")
            return jsonify({'error': 'Invalid request'}), 403
        
        # Get and sanitize form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        year = request.form.get('year', '').strip()
        
        # Validate inputs
        if not security_manager.validate_name(name):
            return jsonify({'error': 'Invalid name format'}), 400
        
        if not security_manager.validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if year not in ['freshman', 'sophomore', 'junior', 'senior', 'graduate']:
            return jsonify({'error': 'Invalid year selection'}), 400
        
        # Sanitize all inputs
        sanitized_name = security_manager.sanitize_input(name)
        sanitized_email = security_manager.sanitize_input(email)
        
        # Log successful submission
        logger.info(f"Form submitted successfully - Name: {sanitized_name}, Email: {sanitized_email}, Year: {year}")
        
        # Here you would typically save to database or send email
        # For now, just return success
        
        return jsonify({
            'success': True,
            'message': f'Thank you for joining, {sanitized_name}! We\'ll be in touch at {sanitized_email} soon.'
        })
        
    except Exception as e:
        logger.error(f"Form submission error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': time.time()})

@app.errorhandler(400)
def bad_request(error):
    """Handle bad request errors"""
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(403)
def forbidden(error):
    """Handle forbidden errors"""
    return jsonify({'error': 'Access forbidden'}), 403

@app.errorhandler(404)
def not_found(error):
    """Handle not found errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(429)
def too_many_requests(error):
    """Handle rate limit exceeded"""
    return jsonify({'error': 'Too many requests. Please try again later.'}), 429

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

def main():
    """Start the secure Flask server"""
    port = int(os.environ.get('PORT', 8000))
    
    print("Starting Secure SRU Cyberspace Club Server...")
    print(f"Server will be available at http://localhost:{port}")
    print("Security features enabled:")
    print("   ✓ Input validation and sanitization")
    print("   ✓ CSRF protection")
    print("   ✓ Rate limiting")
    print("   ✓ Security headers")
    print("   ✓ XSS protection")
    print("   ✓ Suspicious request detection")
    print("   ✓ Session security")
    print("   ✓ Content Security Policy")
    print("-" * 60)
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,  # Disable debug mode in production
            threaded=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"ERROR: Server error: {e}")

if __name__ == "__main__":
    main()

