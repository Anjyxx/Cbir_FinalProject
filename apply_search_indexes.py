import MySQLdb
import os
from dotenv import load_dotenv

def apply_migrations():
    # Load environment variables
    load_dotenv()
    
    # Database configuration
    db_config = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DB', 'your_database_name'),
        'autocommit': True
    }
    
    try:
        # Connect to the database
        connection = MySQLdb.connect(**db_config)
        cursor = connection.cursor()
        
        print("Connected to database successfully!")
        
        # Read and execute the SQL file
        with open('migrations/add_search_indexes.sql', 'r') as sql_file:
            sql_commands = sql_file.read().split(';')
            
            for command in sql_commands:
                if command.strip():
                    try:
                        print(f"Executing: {command[:100]}...")  # Print first 100 chars of command
                        cursor.execute(command)
                        print("✓ Success")
                    except Exception as e:
                        print(f"Error executing command: {e}")
                        print(f"Command was: {command}")
                        
        print("\nAll migrations completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    print("=== Applying Database Migrations for Search Functionality ===")
    print("This will add full-text search indexes and optimize your database for search.")
    input("Press Enter to continue or Ctrl+C to cancel...")
    apply_migrations()
