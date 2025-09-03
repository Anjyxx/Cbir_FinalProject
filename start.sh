#!/bin/bash

# Create necessary directories
mkdir -p static/uploads static/features

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Install dependencies
pip install -r requirements.txt

# Run database migrations if needed
# python manage.py db upgrade

# Start the application
gunicorn --bind 0.0.0.0:$PORT app:app
