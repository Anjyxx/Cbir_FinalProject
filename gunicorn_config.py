import os
import multiprocessing

# Server Socket
bind = '0.0.0.0:' + os.environ.get('PORT', '10000')

# Worker Processes
# Use 2-4 workers per core in production, but not more than 8
workers = min(multiprocessing.cpu_count() * 2 + 1, 8)
worker_class = 'gthread'  # Use threads for I/O-bound applications
threads = 4  # Number of worker threads per process

# Timeouts
timeout = 300  # 5 minutes (adjust based on your application's needs)
graceful_timeout = 30
keepalive = 5

# Debugging
reload = os.environ.get('FLASK_ENV') == 'development'

# Logging
accesslog = '-'  # Log to stdout for Railway to capture
errorlog = '-'   # Log errors to stderr
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)ss'

# Security
forwarded_allow_ips = '*'
proxy_allow_ips = '*'

# Worker Settings
max_requests = 1000  # Restart workers after this many requests
max_requests_jitter = 50  # Random jitter to prevent all workers restarting at once
worker_tmp_dir = '/dev/shm'  # Use shared memory for worker temp files if available

# Server Hooks
def on_starting(server):
    server.log.info('Starting Gunicorn server...')

def on_exit(server):
    server.log.info('Stopping Gunicorn server...')

def worker_abort(worker):
    worker.log.warning('Worker received SIGABRT signal')
