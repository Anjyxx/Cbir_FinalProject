import os
import sys
import subprocess
import time

def check_gunicorn_config():
    """Check if Gunicorn can start with our configuration."""
    print("Checking Gunicorn configuration...")
    
    # Set environment variables
    env = os.environ.copy()
    env['FLASK_APP'] = 'app.py'
    env['FLASK_ENV'] = 'development'
    env['PORT'] = '8000'
    
    try:
        # Check if Gunicorn can load the configuration
        result = subprocess.run(
            [sys.executable, '-m', 'gunicorn', '--check-config', '--config', 'gunicorn_config.py', 'app:app'],
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode == 0:
            print("[OK] Gunicorn configuration is valid!")
            print("\nConfiguration summary:")
            print("-" * 50)
            print(result.stdout)
            return True
        else:
            print("[ERROR] Gunicorn configuration check failed:")
            print("-" * 50)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"[ERROR] Error checking Gunicorn configuration: {str(e)}")
        return False

if __name__ == "__main__":
    check_gunicorn_config()
