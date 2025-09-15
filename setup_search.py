#!/usr/bin/env python3
"""
Setup script for the enhanced search functionality.

This script applies the necessary database migrations and sets up the search functionality.
"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
import MySQLdb

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('setup_search.log')
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

def execute_sql_file(connection, file_path):
    """Execute SQL commands from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_commands = f.read().split(';')
        
        cursor = connection.cursor()
        
        for command in sql_commands:
            command = command.strip()
            if not command:
                continue
                
            try:
                logger.info(f"Executing: {command[:100]}...")
                cursor.execute(command)
                logger.info("✓ Success")
            except MySQLdb.Error as e:
                logger.warning(f"⚠️ Error executing command: {e}")
                # Continue with next command instead of failing
                continue
        
        connection.commit()
        cursor.close()
        return True
        
    except FileNotFoundError:
        logger.error(f"SQL file not found: {file_path}")
        return False
    except Exception as e:
        logger.error(f"Error executing SQL file {file_path}: {e}")
        connection.rollback()
        return False

def check_search_tables(connection):
    """Check if search-related tables exist."""
    cursor = connection.cursor()
    tables = ['search_logs', 'search_suggestions', 'search_analytics']
    missing_tables = []
    
    for table in tables:
        try:
            cursor.execute(f"SHOW TABLES LIKE '{table}'")
            if not cursor.fetchone():
                missing_tables.append(table)
        except MySQLdb.Error as e:
            logger.error(f"Error checking table {table}: {e}")
            missing_tables.append(table)
    
    cursor.close()
    return missing_tables

def check_search_indexes(connection):
    """Check if search-related indexes exist."""
    cursor = connection.cursor()
    indexes = [
        ('house', 'idx_house_search'),
        ('project', 'idx_project_search'),
        ('house', 'idx_house_title'),
        ('house', 'idx_house_price'),
        ('house', 'idx_house_bedrooms'),
        ('house', 'idx_house_bathrooms'),
        ('house', 'idx_house_created_at'),
        ('project', 'idx_project_name'),
        ('project', 'idx_project_location')
    ]
    
    missing_indexes = []
    
    for table, index in indexes:
        try:
            cursor.execute(f"""
                SHOW INDEX FROM {table} WHERE Key_name = %s
            """, (index,))
            if not cursor.fetchone():
                missing_indexes.append(f"{table}.{index}")
        except MySQLdb.Error as e:
            logger.error(f"Error checking index {index} on {table}: {e}")
            missing_indexes.append(f"{table}.{index}")
    
    cursor.close()
    return missing_indexes

def main():
    """Main function to set up search functionality."""
    # Load environment variables
    load_dotenv()
    
    logger.info("🚀 Starting search functionality setup...")
    
    # Get database connection
    connection = get_db_connection()
    
    try:
        # Check if search tables exist
        missing_tables = check_search_tables(connection)
        if missing_tables:
            logger.info(f"Creating missing tables: {', '.join(missing_tables)}")
            execute_sql_file(connection, 'migrations/create_search_tables.sql')
        
        # Check if search indexes exist
        missing_indexes = check_search_indexes(connection)
        if missing_indexes:
            logger.info(f"Creating missing indexes: {', '.join(missing_indexes)}")
            execute_sql_file(connection, 'migrations/add_search_indexes.sql')
        
        # Check if the update_search_suggestions procedure exists
        cursor = connection.cursor()
        cursor.execute("""
            SELECT ROUTINE_NAME 
            FROM information_schema.ROUTINES 
            WHERE ROUTINE_SCHEMA = DATABASE() 
            AND ROUTINE_NAME = 'update_search_suggestions'
        """)
        
        if not cursor.fetchone():
            logger.info("Creating stored procedures and functions...")
            # Re-run the create_search_tables.sql to ensure procedures are created
            execute_sql_file(connection, 'migrations/create_search_tables.sql')
        
        cursor.close()
        
        logger.info("✅ Search functionality setup completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ An error occurred during setup: {e}")
        connection.rollback()
        sys.exit(1)
    finally:
        if connection:
            connection.close()
            logger.info("🔌 Database connection closed.")

if __name__ == "__main__":
    main()
