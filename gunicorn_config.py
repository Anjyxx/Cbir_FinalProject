import os
import multiprocessing

# Number of workers = (2 x $NUM_CORES) + 1
workers = 2
# Use gevent for better concurrency
worker_class = 'gevent'
# Number of worker threads per process
threads = 2
# Bind to the port specified by Railway
bind = f"0.0.0.0:{os.environ.get('PORT', 10000)}"
# Timeout after which a worker is killed and restarted
timeout = 120
# The number of seconds to wait for requests on a Keep-Alive connection
keepalive = 5
# Maximum number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 50
# Log to stdout for Docker
accesslog = '-'
