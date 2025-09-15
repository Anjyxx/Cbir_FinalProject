import os
import pymysql
from dotenv import load_dotenv

def execute_sql_file(connection, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        sql_commands = f.read().split(';')
        
        for command in sql_commands:
            command = command.strip()
            if not command:
                continue
                
            try:
                print(f"Executing: {command[:100]}...")
                with connection.cursor() as cursor:
                    cursor.execute(command)
                connection.commit()
                print("Success")
            except pymysql.Error as e:
                print(f"Error: {e}")
                # Continue with next command
                connection.rollback()
                continue

def main():
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
        print("Connected to database successfully")
        
        sql_file = os.path.join('migrations', 'add_house_type_fts_indexes.sql')
        execute_sql_file(connection, sql_file)
        
        print("\nMigration completed successfully")
        
    except pymysql.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("Database connection closed")

if __name__ == "__main__":
    main()
