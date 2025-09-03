import os
import mysql.connector
from dotenv import load_dotenv

def init_database():
    # Load environment variables
    load_dotenv()
    
    # Database connection parameters
    db_config = {
        'host': os.getenv('MYSQLHOST', 'localhost'),
        'user': os.getenv('MYSQLUSER', 'root'),
        'password': os.getenv('MYSQLPASSWORD', ''),
        'port': int(os.getenv('MYSQLPORT', '3307')),
        'database': os.getenv('MYSQLDATABASE', 'projectdb')
    }
    
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            port=db_config['port']
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_config['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # Use the database
        cursor.execute(f"USE `{db_config['database']}`")
        
        # Read and execute the schema file
        with open('setup_database.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
            
        # Split the script into individual statements
        statements = sql_script.split(';')
        
        for statement in statements:
            # Skip empty statements
            if not statement.strip():
                continue
                
            try:
                cursor.execute(statement)
                connection.commit()
            except mysql.connector.Error as err:
                print(f"Error executing statement: {err}")
                print(f"Statement: {statement[:200]}...")  # Print first 200 chars of failed statement
        
        print("[SUCCESS] Database and tables created successfully!")
        
    except mysql.connector.Error as err:
        print(f"[ERROR] {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    print("Initializing database...")
    init_database()
