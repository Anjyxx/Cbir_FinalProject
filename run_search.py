#!/usr/bin/env python3
"""
Run the search functionality in development mode.

This script starts the Flask development server with the search functionality enabled.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = str(Path(__file__).parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load environment variables
load_dotenv()

# Set up the Flask app
from app import app, mysql

# Import and register search blueprint
from search_utils import search_bp
app.register_blueprint(search_bp, url_prefix='/api/search')

# Configure the app for development
app.config.update(
    DEBUG=True,
    SECRET_KEY=os.getenv('FLASK_SECRET_KEY', 'dev-secret-key'),
    MYSQL_HOST=os.getenv('MYSQL_HOST', 'localhost'),
    MYSQL_USER=os.getenv('MYSQL_USER', 'root'),
    MYSQL_PASSWORD=os.getenv('MYSQL_PASSWORD', ''),
    MYSQL_DB=os.getenv('MYSQL_DB', 'real_estate'),
    MYSQL_CURSORCLASS='DictCursor',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SEARCH_RESULTS_PER_PAGE=20,
    SEARCH_SUGGESTION_LIMIT=10,
    SEARCH_CACHE_TIMEOUT=3600,  # 1 hour
    ENABLE_SEARCH_ANALYTICS=True,
    ENABLE_SEARCH_SUGGESTIONS=True,
    ENABLE_FUZZY_SEARCH=True,
    SEARCH_QUERY_TIMEOUT=5,  # seconds
    MAX_SEARCH_RESULTS=1000
)

# Initialize MySQL
mysql.init_app(app)

# Create database tables if they don't exist
with app.app_context():
    from app import init_db
    init_db()

if __name__ == '__main__':
    print("🚀 Starting search functionality in development mode...")
    print(f"🔍 Search API available at: http://127.0.0.1:5000/api/search")
    print("📚 API Documentation: http://127.0.0.1:5000/api/docs")
    print("🛑 Press Ctrl+C to stop\n")
    
    # Run the Flask development server
    app.run(host='0.0.0.0', port=5000, debug=True)
