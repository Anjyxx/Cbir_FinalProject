#!/bin/bash
set -e

echo "🚀 Starting Vercel build process..."

# Set Python version explicitly
PYTHON_VERSION=3.12
PYTHON=python${PYTHON_VERSION}
PIP=pip${PYTHON_VERSION}

echo "🔍 Using Python: $($PYTHON --version 2>&1) at $(which $PYTHON)"

# Set environment variables
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export PIP_NO_CACHE_DIR=off

# Ensure pip is installed
if ! command -v $PIP &> /dev/null; then
    echo "📦 Installing pip for Python $PYTHON_VERSION..."
    curl -sS https://bootstrap.pypa.io/get-pip.py | $PYTHON
fi

# Upgrade pip
echo "🔄 Upgrading pip..."
$PYTHON -m pip install --upgrade pip

# Create api directory if it doesn't exist
mkdir -p api

# Create app.py in api directory if it doesn't exist
if [ ! -f "api/app.py" ]; then
    echo "📝 Creating app.py for Vercel..."
    echo 'from app import app as application' > api/app.py
fi

# Install requirements from root directory
if [ -f "requirements.txt" ]; then
    echo "📦 Installing requirements from root..."
    $PYTHON -m pip install -r requirements.txt --no-cache-dir
fi

# Install requirements from api directory
if [ -f "api/requirements.txt" ]; then
    echo "📦 Installing requirements from api/requirements.txt..."
    $PYTHON -m pip install -r api/requirements.txt --no-cache-dir
    python3 -m pip install -r requirements.txt --no-cache-dir
fi

# Verify installation
echo "✅ Verifying installation..."
python3 -c "import torch; print(f'PyTorch version: {torch.__version__}')" || echo "PyTorch verification failed"
python3 -c "import torchvision; print(f'torchvision version: {torchvision.__version__}')" || echo "torchvision verification failed"

echo "✨ Build completed successfully!"
