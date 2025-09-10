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
export PYTHONPATH=$PWD

# Function to run commands with error handling
run_command() {
    echo -e "\n💻 Running: $*"
    if ! "$@"; then
        echo -e "❌ Command failed: $*"
        exit 1
    fi
}

# Ensure Python 3.12 is available
if ! command -v $PYTHON &> /dev/null; then
    echo "❌ Python $PYTHON_VERSION is not installed. Installing..."
    apt-get update && apt-get install -y python3.12 python3.12-venv
fi

# Ensure pip is installed
if ! command -v $PIP &> /dev/null; then
    echo "📦 Installing pip for Python $PYTHON_VERSION..."
    run_command curl -sS https://bootstrap.pypa.io/get-pip.py | $PYTHON
fi

# Upgrade pip
echo "🔄 Upgrading pip..."
run_command $PYTHON -m pip install --upgrade pip

# Create api directory if it doesn't exist
run_command mkdir -p api

# Create app.py in api directory if it doesn't exist
if [ ! -f "api/app.py" ]; then
    echo "📝 Creating app.py for Vercel..."
    echo 'from app import app as application' > api/app.py
fi

# Install requirements from api/requirements.in if it exists
if [ -f "api/requirements.in" ]; then
    echo "📦 Installing requirements from api/requirements.in..."
    run_command $PYTHON -m pip install -r api/requirements.in --no-cache-dir
# Fall back to api/requirements.txt if it exists
elif [ -f "api/requirements.txt" ]; then
    echo "📦 Installing requirements from api/requirements.txt..."
    run_command $PYTHON -m pip install -r api/requirements.txt --no-cache-dir
fi

# Install root requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing root requirements..."
    run_command $PYTHON -m pip install -r requirements.txt --no-cache-dir
fi

# Verify installation
echo "✅ Verifying installation..."
run_command $PYTHON -c "import sys; print(f'Python {sys.version}')"
run_command $PYTHON -c "import flask; print(f'Flask {flask.__version__}')" || true

echo "✨ Build completed successfully!"
