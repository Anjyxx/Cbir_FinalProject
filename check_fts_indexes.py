import pymysql
from dotenv import load_dotenv
import os

def check_indexes():
    load_dotenv()
    
    db_config = {
        'host': os.getenv('MYSQLHOST', 'localhost'),
        'user': os.getenv('MYSQLUSER', 'root'),
        'password': os.getenv('MYSQLPASSWORD', ''),
        'db': os.getenv('MYSQLDATABASE', 'projectdb'),
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        
        # Check if ngram parser is available
        cursor.execute("SHOW PLUGINS WHERE Name = 'ngram'")
        ngram_plugin = cursor.fetchone()
        print("\nNgram Parser Status:")
        print("Installed:", "Yes" if ngram_plugin else "No")
        
        # Check indexes for each table
        tables = ['house_type', 'project', 'house']
        
        for table in tables:
            print(f"\n--- {table} Table Indexes ---")
            cursor.execute(f"SHOW INDEX FROM {table}")
            indexes = cursor.fetchall()
            
            if not indexes:
                print("No indexes found")
                continue
                
            for idx in indexes:
                print(f"Index: {idx['Key_name']} on columns: {idx['Column_name']} (Type: {idx['Index_type']})")
                
        # Show the full-text search query that's failing
        print("\n--- Problematic Query ---")
        print("The error occurs because the FULLTEXT index doesn't match the columns in your MATCH clause.")
        print("Please share the exact SQL query from line 3940 in app.py to help diagnose the issue.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    check_indexes()
