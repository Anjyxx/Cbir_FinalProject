#!/bin/bash
set -e

echo "🚀 Starting Vercel build script..."

# Create api directory if it doesn't exist
mkdir -p api

# Create the Vercel serverless function
echo 'from app import app as application' > api/index.py

# Install system dependencies
echo "🔧 Installing system dependencies..."
apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
echo "📦 Upgrading pip..."
python3 -m pip install --upgrade pip

# Install PyTorch with CPU-only version
echo "🧠 Installing PyTorch..."
python3 -m pip install torch==2.0.1 torchvision==0.15.2 --index-url https://download.pytorch.org/whl/cpu --no-cache-dir

# Install requirements from api/requirements.txt if it exists
if [ -f "api/requirements.txt" ]; then
    echo "📦 Installing requirements from api/requirements.txt..."
    python3 -m pip install -r api/requirements.txt --no-cache-dir
fi

# Install root requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing root requirements..."
    python3 -m pip install -r requirements.txt --no-cache-dir
fi

# Verify installation
echo "✅ Verifying installation..."
python3 -c "import torch; print(f'PyTorch version: {torch.__version__}')" || echo "PyTorch verification failed"
python3 -c "import torchvision; print(f'torchvision version: {torchvision.__version__}')" || echo "torchvision verification failed"

echo "✨ Build completed successfully!"
