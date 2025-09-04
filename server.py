#!/usr/bin/env python3
"""
Simple HTTP server for the SRU Cyberspace Club website.
Run this file to serve the website locally.
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Configuration
PORT = 8000
DIRECTORY = Path(__file__).parent

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    """Start the HTTP server and open the website in the default browser."""
    
    # Change to the directory containing this script
    os.chdir(DIRECTORY)
    
    # Create the server
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        print(f"Serving files from: {DIRECTORY}")
        print("Opening website in your default browser...")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Open the website in the default browser
        try:
            webbrowser.open(f'http://localhost:{PORT}')
        except Exception as e:
            print(f"WARNING: Could not open browser automatically: {e}")
            print(f"Please open http://localhost:{PORT} in your browser")
        
        # Start serving
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped by user")
            httpd.shutdown()

if __name__ == "__main__":
    main()
