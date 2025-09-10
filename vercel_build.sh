#!/bin/bash

# Set Python version
PYTHON_VERSION=3.12

# Install required system dependencies
apt-get update && apt-get install -y \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.12 as default
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1
update-alternatives --set python3 /usr/bin/python${PYTHON_VERSION}

# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python${PYTHON_VERSION} get-pip.py

# Create the api directory
mkdir -p api

# Install Python dependencies with specific versions
pip${PYTHON_VERSION} install --upgrade pip
pip${PYTHON_VERSION} install -r requirements.txt

# Create the Vercel serverless function
echo 'from app import app as application' > api/index.py

# Verify installation
python${PYTHON_VERSION} -c "import torch; print(f'PyTorch version: {torch.__version__}')"
