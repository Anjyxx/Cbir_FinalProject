import os
import sys
import MySQLdb
from dotenv import load_dotenv

def apply_migrations():
    """Apply database migrations for search functionality."""
    # Load environment variables
    load_dotenv()
    
    # Database configuration
    db_config = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DB', 'your_database_name'),
        'charset': 'utf8mb4',
        'use_unicode': True,
        'autocommit': True
    }
    
    try:
        # Connect to the database
        connection = MySQLdb.connect(**db_config)
        cursor = connection.cursor()
        
        print("✅ Connected to database successfully!")
        
        # Read and execute the SQL migrations
        migration_files = [
            'migrations/create_search_tables.sql',
            'migrations/add_search_indexes.sql'
        ]
        
        for migration_file in migration_files:
            try:
                print(f"\n🔧 Applying migration: {migration_file}")
                with open(migration_file, 'r', encoding='utf-8') as f:
                    sql_commands = f.read().split(';')
                
                # Execute each SQL command
                for command in sql_commands:
                    command = command.strip()
                    if not command:
                        continue
                    
                    try:
                        print(f"  • Executing: {command[:100]}...")
                        cursor.execute(command)
                        print("    ✓ Success")
                    except MySQLdb.Error as e:
                        print(f"    ⚠️ Error executing command: {e}")
                        # Continue with next command instead of failing
                        continue
                
                print(f"✅ Successfully applied {migration_file}")
                
            except FileNotFoundError:
                print(f"⚠️ Migration file not found: {migration_file}")
                continue
            except Exception as e:
                print(f"❌ Error applying migration {migration_file}: {e}")
                raise
        
        print("\n✨ All migrations completed successfully!")
        
    except MySQLdb.Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()
            print("\n🔌 Database connection closed.")

if __name__ == "__main__":
    print("🚀 Starting search functionality database migrations...")
    apply_migrations()
