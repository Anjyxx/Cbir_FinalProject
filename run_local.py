import os
from app import app, setup_thai_font

if __name__ == '__main__':
    # Set up environment variables
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'
    
    # Set up Thai font for PDF generation
    setup_thai_font()
    
    # Create necessary directories
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('static/features', exist_ok=True)
    
    # Run the Flask development server
    app.run(host='0.0.0.0', port=5000, debug=True)
