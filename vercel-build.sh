#!/bin/bash
set -e

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip

# First install PyTorch with specific index URL for CPU version
echo "Installing PyTorch..."
pip install torch==2.2.0 torchvision==0.17.0 --index-url https://download.pytorch.org/whl/cpu

# Then install other requirements
echo "Installing other requirements..."
pip install -r requirements.txt

# Create the api directory if it doesn't exist
mkdir -p api

# Create the Vercel serverless function
echo 'from app import app as application' > api/index.py

# Verify installation
echo "Verifying installation..."
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
