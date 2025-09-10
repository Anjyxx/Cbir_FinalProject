import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Add the project root to the Python path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Import the Flask app
    from app import create_app
    
    # Create the application
    application = create_app()
    logger.info("Application initialized successfully")
    
except Exception as e:
    # Log any errors during initialization
    logger.error(f"Failed to initialize application: {str(e)}")
    logger.exception("Stack trace:")
    
    # Create a minimal error app if initialization fails
    from flask import Flask, jsonify
    
    error_app = Flask(__name__)
    
    @error_app.route('/<path:path>')
    def error_handler(path):
        return jsonify({
            'error': 'Application initialization failed',
            'message': str(e)
        }), 500
    
    application = error_app
