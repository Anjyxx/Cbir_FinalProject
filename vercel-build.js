const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 Starting Vercel build process...');

// Set environment variables
process.env.PYTHONUNBUFFERED = '1';
process.env.PYTHONDONTWRITEBYTECODE = '1';

// Create api directory if it doesn't exist
const apiDir = path.join(process.cwd(), 'api');
if (!fs.existsSync(apiDir)) {
  console.log('📁 Creating api directory...');
  fs.mkdirSync(apiDir, { recursive: true });
}

// Create app.py in api directory if it doesn't exist
const appPyPath = path.join(apiDir, 'app.py');
if (!fs.existsSync(appPyPath)) {
  console.log('📝 Creating app.py for Vercel...');
  fs.writeFileSync(appPyPath, 'from app import app as application\n');
}

// Function to run commands with error handling
function runCommand(command, options = {}) {
  console.log(`\n💻 Running: ${command}`);
  try {
    execSync(command, {
      stdio: 'inherit',
      ...options,
      env: { 
        ...process.env,
        PIP_NO_CACHE_DIR: 'off',
        ...(options.env || {})
      }
    });
    return true;
  } catch (error) {
    console.error(`❌ Command failed: ${command}`);
    console.error(error.message);
    return false;
  }
}

// Main build process
async function main() {
  try {
    // Update pip
    console.log('\n🔄 Updating pip...');
    if (!runCommand('python -m pip install --upgrade pip')) {
      throw new Error('Failed to update pip');
    }

    // Install PyTorch with specific CPU version
    console.log('\n🔧 Installing PyTorch...');
    const torchCommand = 'python -m pip install torch==2.0.1 torchvision==0.15.2 --index-url https://download.pytorch.org/whl/cpu --no-cache-dir';
    if (!runCommand(torchCommand)) {
      console.warn('⚠️  First PyTorch installation attempt failed, trying alternative...');
      // Try alternative installation method
      const altTorchCommand = 'python -m pip install torch==2.0.1+cpu torchvision==0.15.2+cpu --index-url https://download.pytorch.org/whl/cpu --no-cache-dir';
      if (!runCommand(altTorchCommand)) {
        throw new Error('Failed to install PyTorch after multiple attempts');
      }
    }

    // Install requirements from api/requirements.txt
    const requirementsPath = path.join(process.cwd(), 'api', 'requirements.txt');
    if (fs.existsSync(requirementsPath)) {
      console.log('\n📦 Installing requirements from api/requirements.txt...');
      if (!runCommand(`python -m pip install -r ${requirementsPath} --no-cache-dir`)) {
        console.warn('⚠️  Failed to install requirements from api/requirements.txt, trying root requirements.txt...');
      }
    }

    // Install root requirements.txt if it exists
    const rootRequirements = path.join(process.cwd(), 'requirements.txt');
    if (fs.existsSync(rootRequirements)) {
      console.log('\n📦 Installing root requirements...');
      if (!runCommand(`python -m pip install -r ${rootRequirements} --no-cache-dir`)) {
        console.warn('⚠️  Failed to install root requirements');
      }
    }

    console.log('\n✅ Build completed successfully!');
  } catch (error) {
    console.error('\n❌ Build failed with error:');
    console.error(error);
    process.exit(1);
  }
}

// Run the build process
main();
