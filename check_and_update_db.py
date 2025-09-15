import MySQLdb

def check_and_update_db():
    try:
        # Try to connect to MySQL with common default credentials
        # You may need to adjust these based on your MySQL setup
        db_configs = [
            {'host': 'localhost', 'user': 'root', 'password': ''},
            {'host': '127.0.0.1', 'user': 'root', 'password': ''},
            {'host': 'localhost', 'user': 'root', 'password': 'root'},
            {'host': '127.0.0.1', 'user': 'root', 'password': 'root'}
        ]
        
        connection = None
        for config in db_configs:
            try:
                print(f"Trying to connect to MySQL with {config}")
                connection = MySQLdb.connect(
                    host=config['host'],
                    user=config['user'],
                    password=config['password'],
                    database='projectdb'
                )
                print(f"Successfully connected to MySQL at {config['host']}")
                break
            except MySQLdb.OperationalError as e:
                print(f"Failed to connect with {config}: {e}")
                continue
        
        if not connection:
            print("Could not connect to MySQL with any of the provided configurations.")
            print("Please make sure MySQL is running and update the connection details in the script.")
            return
        
        # Check if the columns exist
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'projectdb' 
            AND TABLE_NAME = 'house' 
            AND COLUMN_NAME IN ('bedrooms', 'bathrooms', 'living_area')
        """)
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"Existing columns in house table: {existing_columns}")
        
        # Add missing columns
        if 'bedrooms' not in existing_columns:
            print("Adding 'bedrooms' column to house table...")
            cursor.execute("""
                ALTER TABLE house 
                ADD COLUMN bedrooms INT DEFAULT 0
            """)
            print("Added 'bedrooms' column")
        
        if 'bathrooms' not in existing_columns:
            print("Adding 'bathrooms' column to house table...")
            cursor.execute("""
                ALTER TABLE house 
                ADD COLUMN bathrooms INT DEFAULT 0
            """)
            print("Added 'bathrooms' column")
            
        if 'living_area' not in existing_columns:
            print("Adding 'living_area' column to house table...")
            cursor.execute("""
                ALTER TABLE house 
                ADD COLUMN living_area DECIMAL(10,2) DEFAULT 0.00
            """)
            print("Added 'living_area' column")
        
        # Add indexes for better performance
        cursor.execute("""
            SHOW INDEX FROM house WHERE Column_name = 'bedrooms'
        """)
        if not cursor.fetchone():
            print("Adding index for 'bedrooms' column...")
            cursor.execute("CREATE INDEX idx_house_bedrooms ON house(bedrooms)")
            
        cursor.execute("""
            SHOW INDEX FROM house WHERE Column_name = 'bathrooms'
        """)
        if not cursor.fetchone():
            print("Adding index for 'bathrooms' column...")
            cursor.execute("CREATE INDEX idx_house_bathrooms ON house(bathrooms)")
            
        cursor.execute("""
            SHOW INDEX FROM house WHERE Column_name = 'living_area'
        """)
        if not cursor.fetchone():
            print("Adding index for 'living_area' column...")
            cursor.execute("CREATE INDEX idx_house_living_area ON house(living_area)")
        
        connection.commit()
        print("Database update completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        if 'connection' in locals() and connection:
            connection.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == "__main__":
    check_and_update_db()
