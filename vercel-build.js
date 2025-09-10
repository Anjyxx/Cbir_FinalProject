const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('Starting Vercel build...');

// Create api directory if it doesn't exist
if (!fs.existsSync('api')) {
  fs.mkdirSync('api');
}

// Create a minimal Python server
fs.writeFileSync('api/index.py', 'from app import app as application');

// Install Python dependencies
console.log('Installing Python dependencies...');
try {
  // Install PyTorch with CPU-only version first
  execSync('pip install torch==2.0.0+cpu torchvision==0.15.1+cpu -f https://download.pytorch.org/whl/torch_stable.html', {
    stdio: 'inherit',
    env: { ...process.env, PIP_NO_CACHE_DIR: 'off' }
  });
  
  // Install other requirements
  execSync('pip install -r requirements.txt', {
    stdio: 'inherit',
    env: { ...process.env, PIP_NO_CACHE_DIR: 'off' }
  });
  
  console.log('Dependencies installed successfully!');
} catch (error) {
  console.error('Error installing dependencies:', error);
  process.exit(1);
}
