import os
import MySQLdb
from dotenv import load_dotenv

def execute_sql_file(cursor, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # Split the file into individual SQL statements
        sql_commands = f.read().split(';')
        
        for command in sql_commands:
            # Skip empty statements
            if not command.strip():
                continue
                
            try:
                print(f"Executing: {command[:100]}...")
                cursor.execute(command)
                print("Success")
            except MySQLdb.Error as e:
                print(f"Error executing command: {e}")
                # Continue with next command even if one fails
                continue

def main():
    # Load environment variables
    load_dotenv()
    
    # Database connection parameters
    db_config = {
        'host': os.getenv('MYSQLHOST', 'localhost'),
        'user': os.getenv('MYSQLUSER', 'root'),
        'password': os.getenv('MYSQLPASSWORD', ''),
        'database': os.getenv('MYSQLDATABASE', 'projectdb'),
        'charset': 'utf8mb4',
        'cursorclass': MySQLdb.cursors.DictCursor
    }
    
    try:
        # Connect to the database
        conn = MySQLdb.connect(**db_config)
        cursor = conn.cursor()
        
        print("Connected to database successfully")
        
        # Execute the SQL file
        sql_file = os.path.join('migrations', 'add_house_type_fts_indexes.sql')
        execute_sql_file(cursor, sql_file)
        
        # Commit changes
        conn.commit()
        print("Migration completed successfully")
        
    except MySQLdb.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'conn' in locals() and conn.open:
            cursor.close()
            conn.close()
            print("Database connection closed")

if __name__ == "__main__":
    main()
