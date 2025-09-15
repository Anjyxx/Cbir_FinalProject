#!/usr/bin/env python3
"""
Script to remove full-text search functionality from the project.
This script will:
1. Remove search-related indexes and tables from the database
2. Clean up any search-related files
"""
import os
import sys
import logging
import MySQLdb
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('remove_search.log')
    ]
)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Create and return a database connection."""
    try:
        connection = MySQLdb.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            passwd=os.getenv('MYSQL_PASSWORD', ''),
            db=os.getenv('MYSQL_DB', 'real_estate'),
            charset='utf8mb4',
            use_unicode=True,
            autocommit=False
        )
        return connection
    except MySQLdb.Error as e:
        logger.error(f"Error connecting to database: {e}")
        sys.exit(1)

def execute_remove_script(connection):
    """Execute the SQL script to remove search functionality."""
    try:
        script_path = os.path.join('migrations', 'remove_search_functionality.sql')
        if not os.path.exists(script_path):
            logger.error(f"SQL script not found: {script_path}")
            return False
            
        with open(script_path, 'r', encoding='utf-8') as f:
            sql_commands = f.read().split(';')
        
        cursor = connection.cursor()
        
        for command in sql_commands:
            # Skip empty statements
            if not command.strip():
                continue
                
            try:
                logger.info(f"Executing: {command.strip()[:100]}...")
                cursor.execute(command)
                logger.info("Command executed successfully")
            except MySQLdb.Error as e:
                logger.warning(f"Warning executing command: {e}")
                # Continue with next command
        
        connection.commit()
        cursor.close()
        return True
        
    except Exception as e:
        logger.error(f"Error executing remove script: {e}")
        if 'connection' in locals():
            connection.rollback()
        return False

def remove_search_files():
    """Remove search-related Python files."""
    search_files = [
        'cbir_search.py',
        'run_search.py',
        'search_utils.py',
        'setup_search.py',
        'apply_search_indexes.py',
        'apply_search_migrations.py',
        'tests/test_search.py'
    ]
    
    for file_path in search_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Removed file: {file_path}")
        except Exception as e:
            logger.warning(f"Could not remove {file_path}: {e}")

def main():
    """Main function to remove search functionality."""
    logger.info("Starting removal of search functionality...")
    
    # Load environment variables
    load_dotenv()
    
    # Remove database search functionality
    connection = None
    try:
        connection = get_db_connection()
        if execute_remove_script(connection):
            logger.info("Successfully removed search functionality from database")
        else:
            logger.error("Failed to remove search functionality from database")
    except Exception as e:
        logger.error(f"Error during database cleanup: {e}")
    finally:
        if connection:
            connection.close()
    
    # Remove search-related files
    remove_search_files()
    
    logger.info("Search functionality removal completed")

if __name__ == "__main__":
    main()
