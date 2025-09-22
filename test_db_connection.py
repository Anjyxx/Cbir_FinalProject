#!/usr/bin/env python3

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, mysql
    
    def test_db_connection():
        try:
            with app.app_context():
                print("🔍 Testing database connection...")
                print(f"MySQL Host: {app.config['MYSQL_HOST']}")
                print(f"MySQL Port: {app.config['MYSQL_PORT']}")
                print(f"MySQL Database: {app.config['MYSQL_DB']}")
                print(f"MySQL User: {app.config['MYSQL_USER']}")
                
                cur = mysql.connection.cursor()
                
                # Check if image_embeddings table exists
                cur.execute('SHOW TABLES LIKE "image_embeddings"')
                result = cur.fetchone()
                print(f'\n✅ image_embeddings table exists: {result is not None}')
                
                if result:
                    # Check count of embeddings
                    cur.execute('SELECT COUNT(*) FROM image_embeddings')
                    count = cur.fetchone()[0]
                    print(f'📊 Total embeddings: {count}')
                    
                    if count > 0:
                        # Check sample data
                        cur.execute('SELECT image_id, house_id, embedding_type FROM image_embeddings LIMIT 3')
                        samples = cur.fetchall()
                        print(f'📋 Sample embeddings: {samples}')
                    else:
                        print('❌ No embeddings in database - this is why database search fails!')
                else:
                    print('❌ image_embeddings table does not exist!')
                
                cur.close()
                
        except Exception as e:
            print(f'❌ Database connection error: {e}')
            import traceback
            traceback.print_exc()

    if __name__ == "__main__":
        test_db_connection()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
    print("and that all dependencies are installed.")
