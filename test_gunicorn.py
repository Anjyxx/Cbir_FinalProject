import multiprocessing
import os
import signal
import subprocess
import time
import requests
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def start_gunicorn():
    """Start Gunicorn server in a separate process."""
    env = os.environ.copy()
    env['FLASK_ENV'] = 'development'
    env['PORT'] = '8000'
    
    # Start Gunicorn with our config
    cmd = [
        'gunicorn',
        '--config', 'gunicorn_config.py',
        'app:app'
    ]
    
    process = subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Give it a moment to start
    time.sleep(5)
    return process

def test_requests(port=8000):
    """Test making requests to the running server."""
    base_url = f'http://localhost:{port}'
    
    # Test basic endpoints
    endpoints = ['/', '/admin', '/houses']
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            print(f"✅ {endpoint}: {response.status_code}")
            print(f"   Response time: {response.elapsed.total_seconds():.3f}s")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {str(e)}")
    
    # Test a heavier endpoint
    try:
        start = time.time()
        response = requests.get(f"{base_url}/api/houses", timeout=30)
        duration = time.time() - start
        print(f"\n🔍 API Test:")
        print(f"   Status: {response.status_code}")
        print(f"   Response time: {duration:.3f}s")
        print(f"   Items returned: {len(response.json().get('data', []))}")
    except Exception as e:
        print(f"\n❌ API Test Failed: {str(e)}")

def main():
    print("🚀 Starting Gunicorn server for testing...")
    
    # Start Gunicorn
    server = start_gunicorn()
    
    try:
        # Run tests
        test_requests()
        
    finally:
        # Clean up
        print("\n🛑 Stopping Gunicorn server...")
        server.terminate()
        server.wait()
        
        # Print server output
        print("\n📝 Server output:")
        print(server.stdout.read())
        print("\n❌ Server errors:")
        print(server.stderr.read())

if __name__ == "__main__":
    main()
