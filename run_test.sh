#!/bin/bash

# Exit on error
set -e

# Create necessary directories
mkdir -p static/uploads static/features

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Install dependencies if not already installed
pip install -r requirements.txt

# Test the Gunicorn configuration
echo "🔍 Testing Gunicorn configuration..."
gunicorn --check-config --config gunicorn_config.py app:app

echo -e "\n✅ Gunicorn configuration is valid"
echo -e "\n🚀 Starting Gunicorn server for testing (press Ctrl+C to stop)..."

# Start Gunicorn with our config
gunicorn --config gunicorn_config.py app:app
