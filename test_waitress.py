import os
import subprocess
import time
import requests

def start_waitress():
    """Start Waitress server in a separate process."""
    env = os.environ.copy()
    env['FLASK_APP'] = 'app.py'
    env['FLASK_ENV'] = 'development'
    env['PORT'] = '8000'
    
    cmd = [
        'waitress-serve',
        '--port=8000',
        'app:app'
    ]
    
    process = subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    
    # Give it a moment to start
    time.sleep(5)
    return process

def test_endpoints():
    """Test basic endpoints."""
    base_url = 'http://localhost:8000'
    endpoints = ['/', '/admin', '/houses']
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            print(f"{endpoint}: {response.status_code} (Response time: {response.elapsed.total_seconds():.3f}s)")
        except Exception as e:
            print(f"Error accessing {endpoint}: {str(e)}")

def main():
    print("Starting Waitress server for testing...")
    server = None
    
    try:
        server = start_waitress()
        print("Server started. Testing endpoints...\n")
        test_endpoints()
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        
    finally:
        if server:
            print("\nStopping server...")
            server.terminate()
            
        # Print server output
        print("\nServer output:")
        if server:
            print(server.stdout.read())
            print("\nServer errors:")
            print(server.stderr.read())

if __name__ == "__main__":
    main()
