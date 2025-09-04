#!/bin/bash

# SRU Cyberspace Club Secure Server Startup Script
# This script starts the secure Flask server with proper security configuration

echo "Starting SRU Cyberspace Club Secure Server..."
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing/updating dependencies..."
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export FLASK_DEBUG=0

# Generate secret key if not set
if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    echo "Generated new SECRET_KEY"
fi

# Create logs directory
mkdir -p logs

# Set proper permissions
chmod 755 logs/
chmod 644 *.py *.html *.css *.js

echo "Starting secure server..."
echo "Server will be available at http://localhost:8000"
echo "Security logs will be written to logs/security.log"
echo "Press Ctrl+C to stop the server"
echo "=================================================="

# Start the secure server
python3 secure_server.py

