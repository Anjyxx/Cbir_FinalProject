#!/bin/bash
set -e

echo "🚀 Starting Vercel build script..."

# Set Python version
PYTHON_VERSION=3.9

# Install system dependencies
echo "🔧 Installing system dependencies..."
apt-get update && apt-get install -y \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.9 as default
echo "🐍 Setting Python ${PYTHON_VERSION} as default..."
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1
update-alternatives --set python3 /usr/bin/python${PYTHON_VERSION}

# Install pip
echo "📦 Installing/upgrading pip..."
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python${PYTHON_VERSION} get-pip.py

# Create api directory if it doesn't exist
mkdir -p api

# Create the Vercel serverless function
echo 'from app import app as application' > api/index.py

# Install PyTorch with specific CPU version
echo "🧠 Installing PyTorch..."
pip install torch==2.0.0+cpu torchvision==0.15.1+cpu --index-url https://download.pytorch.org/whl/cpu --no-cache-dir

# Install requirements from api/requirements.txt if it exists
if [ -f "api/requirements.txt" ]; then
    echo "📦 Installing requirements from api/requirements.txt..."
    pip install -r api/requirements.txt --no-cache-dir
fi

# Install root requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing root requirements..."
    pip install -r requirements.txt --no-cache-dir
fi

# Verify installation
echo "✅ Verifying installation..."
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
python -c "import torchvision; print(f'torchvision version: {torchvision.__version__}')"

echo "✨ Build completed successfully!"
