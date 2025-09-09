import os

workers = 2
worker_class = 'sync'
threads = 2
bind = f"0.0.0.0:{os.environ.get('PORT', 10000)}"
timeout = 120
keepalive = 5
