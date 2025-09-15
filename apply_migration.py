import MySQLdb
import os
from dotenv import load_dotenv

def apply_migration():
    # Load environment variables
    load_dotenv()
    
    # Database connection parameters
    db_config = {
        'host': os.getenv('MYSQLHOST', 'localhost'),
        'user': os.getenv('MYSQLUSER', 'root'),
        'password': os.getenv('MYSQLPASSWORD', ''),
        'database': os.getenv('MYSQLDATABASE', 'projectdb'),
        'port': int(os.getenv('MYSQLPORT', 3306))
    }
    
    try:
        # Connect to MySQL
        connection = MySQLdb.connect(**db_config)
        cursor = connection.cursor()
        
        # Migration 1: Add bedrooms, bathrooms, and living_area to house table
        print("Applying migration: Add bedrooms, bathrooms, and living_area to house table...")
        try:
            with open('migrations/add_bedrooms_bathrooms_columns.sql', 'r') as f:
                sql_commands = f.read().split(';')
            
            # Execute each command
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
            print("Migration 1 applied successfully!")
        except Exception as e:
            print(f"Warning: Could not apply migration 1: {e}")
        
        # Migration 2: Add p_description and p_location to project table
        print("\nApplying migration: Add p_description and p_location to project table...")
        try:
            # Check if columns already exist
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'project' 
                AND COLUMN_NAME IN ('p_description', 'p_location')
            """)
            existing_columns = [row[0] for row in cursor.fetchall()]
            
            if 'p_description' not in existing_columns:
                cursor.execute("""
                    ALTER TABLE project 
                    ADD COLUMN p_description TEXT DEFAULT NULL AFTER p_name
                """)
                print("Added p_description column to project table")
            
            if 'p_location' not in existing_columns:
                cursor.execute("""
                    ALTER TABLE project 
                    ADD COLUMN p_location VARCHAR(255) DEFAULT NULL AFTER p_description
                """)
                print("Added p_location column to project table")
            
            # Update existing rows with empty values for the new columns
            cursor.execute("""
                UPDATE project 
                SET p_description = '' 
                WHERE p_description IS NULL
            """)
            
            cursor.execute("""
                UPDATE project 
                SET p_location = '' 
                WHERE p_location IS NULL
            """)
            
            print("Migration 2 applied successfully!")
        except Exception as e:
            print(f"Error applying migration 2: {e}")
            raise
        
        # Commit all changes
        connection.commit()
        print("\nAll migrations applied successfully!")
        
    except Exception as e:
        print(f"Error applying migrations: {e}")
        if 'connection' in locals() and connection:
            connection.rollback()
        return False
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()
    
    return True

if __name__ == "__main__":
    if apply_migration():
        print("\nDatabase schema is up to date!")
    else:
        print("\nFailed to apply migrations. Please check the error messages above.")
        exit(1)
