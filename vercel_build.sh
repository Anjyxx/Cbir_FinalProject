#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Create the api directory if it doesn't exist
mkdir -p api

# Create the Vercel serverless function
echo 'from app import app as application' > api/index.py
