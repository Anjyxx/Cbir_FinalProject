import pymysql
from dotenv import load_dotenv
import os

def check_fts_indexes():
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
        print("Connected to database successfully\n")
        
        with connection.cursor() as cursor:
            # Check house table indexes
            print("=== House Table Indexes ===")
            cursor.execute("SHOW INDEX FROM house")
            for idx in cursor.fetchall():
                print(f"Index: {idx['Key_name']}, Column: {idx['Column_name']}, Type: {idx['Index_type']}")
            
            # Check project table indexes
            print("\n=== Project Table Indexes ===")
            cursor.execute("SHOW INDEX FROM project")
            for idx in cursor.fetchall():
                print(f"Index: {idx['Key_name']}, Column: {idx['Column_name']}, Type: {idx['Index_type']}")
            
            # Check house_type table indexes
            print("\n=== House Type Table Indexes ===")
            cursor.execute("SHOW INDEX FROM house_type")
            for idx in cursor.fetchall():
                print(f"Index: {idx['Key_name']}, Column: {idx['Column_name']}, Type: {idx['Index_type']}")
            
            # Check if ngram parser is available
            print("\n=== Checking ngram Parser Status ===")
            cursor.execute("SHOW PLUGINS WHERE Name = 'ngram'")
            ngram_plugin = cursor.fetchone()
            if ngram_plugin:
                print("ngram parser is available")
            else:
                print("WARNING: ngram parser is not available")
            
            # Check table columns for the search
            print("\n=== Checking Table Columns ===")
            cursor.execute("""
                SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_SET_NAME, COLLATION_NAME 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME IN ('house', 'project', 'house_type')
                AND COLUMN_NAME IN ('h_title', 'h_description', 'p_name', 'p_description', 't_name', 't_description')
            """)
            print("\nRelevant columns for search:")
            for col in cursor.fetchall():
                print(f"Table: {col['TABLE_NAME'] if 'TABLE_NAME' in col else 'N/A'}, "
                      f"Column: {col['COLUMN_NAME']}, "
                      f"Type: {col['DATA_TYPE']}, "
                      f"Charset: {col['CHARACTER_SET_NAME']}")
    
    except pymysql.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("\nDatabase connection closed")

if __name__ == "__main__":
    check_fts_indexes()
