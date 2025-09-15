import os
import sys
import pytest
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
load_dotenv()

# Test configuration
@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for testing."""
    from app import app as flask_app
    
    # Configure the app for testing
    flask_app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'MYSQL_HOST': os.getenv('TEST_MYSQL_HOST', 'localhost'),
        'MYSQL_USER': os.getenv('TEST_MYSQL_USER', 'root'),
        'MYSQL_PASSWORD': os.getenv('TEST_MYSQL_PASSWORD', ''),
        'MYSQL_DB': os.getenv('TEST_MYSQL_DB', 'test_db'),
    })
    
    # Establish an application context before running the tests
    ctx = flask_app.app_context()
    ctx.push()
    
    yield flask_app
    
    # Clean up after tests
    ctx.pop()

@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def db_connection(app):
    """A database connection for testing."""
    from app import mysql
    
    # Get a connection and cursor
    connection = mysql.connection
    cursor = connection.cursor()
    
    # Start a transaction
    cursor.execute("START TRANSACTION")
    
    yield connection, cursor
    
    # Rollback any changes made during the test
    cursor.execute("ROLLBACK")
    cursor.close()

# Custom markers
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: mark test as slow to run"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
