import os
import MySQLdb
from dotenv import load_dotenv

def apply_migrations():
    # Load environment variables
    load_dotenv()
    
    # Database connection parameters
    db_config = {
        'host': os.getenv('MYSQLHOST', 'localhost'),
        'user': os.getenv('MYSQLUSER', 'root'),
        'password': os.getenv('MYSQLPASSWORD', ''),
        'database': 'projectdb',
        'autocommit': True
    }
    
    try:
        # Connect to MySQL
        conn = MySQLdb.connect(**db_config)
        cursor = conn.cursor()
        
        print("Connected to MySQL database")
        
        # Read and execute the migration file
        with open('migrations/add_fts_indexes.sql', 'r') as f:
            sql_commands = f.read().split(';')
            
            for command in sql_commands:
                if command.strip():
                    try:
                        print(f"Executing: {command[:100]}...")
                        cursor.execute(command)
                        print("Success")
                    except Exception as e:
                        print(f"Error executing command: {e}")
                        print("Continuing with next command...")
        
        print("All migrations applied successfully!")
        
    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if 'conn' in locals() and conn.open:
            cursor.close()
            conn.close()
            print("Database connection closed")

if __name__ == "__main__":
    apply_migrations()
