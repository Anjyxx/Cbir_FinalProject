import MySQLdb
import os

def check_house_table_structure():
    try:
        # Connect to the database using the same config as the app
        db = MySQLdb.connect(
            host=os.environ.get('MYSQLHOST', 'localhost'),
            user=os.environ.get('MYSQLUSER', 'root'),
            passwd=os.environ.get('MYSQLPASSWORD', ''),
            db=os.environ.get('MYSQLDATABASE', 'projectdb'),
            port=int(os.environ.get('MYSQLPORT', 3307)),
            charset='utf8mb4'
        )
        cursor = db.cursor()
        
        # Get the structure of the house table
        cursor.execute("SHOW COLUMNS FROM house")
        print("\n=== House Table Structure ===")
        print(f"{'Field':<30} | {'Type':<20} | {'Null':<5} | {'Key':<5} | {'Default':<10} | {'Extra':<10}")
        print("-" * 90)
        
        for column in cursor.fetchall():
            print(f"{column[0]:<30} | {column[1]:<20} | {column[2]:<5} | {column[3]:<5} | {str(column[4] or 'NULL'):<10} | {column[5] or ''}")
        
        # Check if there's a separate table for house images
        cursor.execute("SHOW TABLES LIKE 'house_images'")
        if cursor.fetchone():
            print("\n=== House Images Table Structure ===")
            cursor.execute("SHOW COLUMNS FROM house_images")
            print(f"{'Field':<30} | {'Type':<20} | {'Null':<5} | {'Key':<5} | {'Default':<10} | {'Extra':<10}")
            print("-" * 90)
            for column in cursor.fetchall():
                print(f"{column[0]:<30} | {column[1]:<20} | {column[2]:<5} | {column[3]:<5} | {str(column[4] or 'NULL'):<10} | {column[5] or ''}")
        
        db.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("=== Checking Database Structure ===")
    check_house_table_structure()
