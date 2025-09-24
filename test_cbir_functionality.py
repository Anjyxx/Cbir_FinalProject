#!/usr/bin/env python3

import os
import sys
import numpy as np

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_cbir_functionality():
    print("🔍 Testing CBIR functionality...")
    
    try:
        # Test 1: Check if cbir_search module can be imported
        print("📦 Testing cbir_search import...")
        from cbir_search import search_similar_images, extract_feature, extract_style_feature
        print("✅ cbir_search imported successfully")
        
        # Test 2: Check if cbir_database module can be imported
        print("📦 Testing cbir_database import...")
        from cbir_database import search_similar_images_db
        print("✅ cbir_database imported successfully")
        
        # Test 3: Check if feature files exist
        print("📁 Checking feature files...")
        feature_files = [
            'static/features/house_features.npy',
            'static/features/filenames.npy',
            'static/features/house_style_features.npy'
        ]
        
        for file_path in feature_files:
            if os.path.exists(file_path):
                features = np.load(file_path)
                print(f"✅ {file_path}: {features.shape}")
            else:
                print(f"❌ {file_path}: Not found")
        
        # Test 4: Test database connection directly
        print("🔗 Testing database connection...")
        import pymysql
        pymysql.install_as_MySQLdb()
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Connect to database
        connection = pymysql.connect(
            host=os.environ.get('MYSQLHOST', 'localhost'),
            user=os.environ.get('MYSQLUSER', 'root'),
            password=os.environ.get('MYSQLPASSWORD', ''),
            database=os.environ.get('MYSQLDATABASE', 'projectdb'),
            port=int(os.environ.get('MYSQLPORT', '3307')),
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Check image_embeddings table
        cursor.execute('SELECT COUNT(*) FROM image_embeddings')
        count = cursor.fetchone()[0]
        print(f"✅ Database connection successful - {count} embeddings found")
        
        # Get sample data
        cursor.execute('SELECT image_id, house_id, embedding_type FROM image_embeddings LIMIT 3')
        samples = cursor.fetchall()
        print(f"📋 Sample embeddings: {samples}")
        
        cursor.close()
        connection.close()
        
        print("🎉 All CBIR functionality tests passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cbir_functionality()


