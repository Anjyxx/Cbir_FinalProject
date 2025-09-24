#!/usr/bin/env python3

import os
import sys
import pymysql
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_limited_results():
    print("🔍 Debugging why only 2 results are shown...")
    
    try:
        # Load environment variables
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
        
        # Check how many houses have main images with embeddings
        print("📊 Checking main images with embeddings...")
        cursor.execute("""
            SELECT COUNT(DISTINCT ie.house_id) as house_count
            FROM image_embeddings ie
            JOIN house_images hi ON ie.image_id = hi.id AND hi.is_main = 1
            WHERE ie.embedding_type = 'visual'
        """)
        
        house_count = cursor.fetchone()[0]
        print(f"📊 Houses with main images and embeddings: {house_count}")
        
        # Check which houses have main images with embeddings
        cursor.execute("""
            SELECT ie.house_id, h.h_title, ie.image_url, hi.is_main
            FROM image_embeddings ie
            JOIN house h ON ie.house_id = h.h_id
            JOIN house_images hi ON ie.image_id = hi.id AND hi.is_main = 1
            WHERE ie.embedding_type = 'visual'
            ORDER BY ie.house_id
        """)
        
        main_images = cursor.fetchall()
        print(f"📊 Main images with embeddings: {len(main_images)}")
        
        for row in main_images:
            house_id, house_title, image_url, is_main = row
            filename = image_url.split('/')[-1] if '/' in image_url else image_url
            print(f"  House {house_id}: {house_title} - {filename} (main: {is_main})")
        
        # Test CBIR search to see what it returns
        print(f"\n🔍 Testing CBIR search...")
        from cbir_database import search_similar_images_db
        
        # Use a test image
        test_image = 'static/uploads/OIP_4.webp'
        if not os.path.exists(test_image):
            uploads_dir = 'static/uploads'
            for filename in os.listdir(uploads_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    test_image = os.path.join(uploads_dir, filename)
                    break
        
        print(f"📷 Using test image: {test_image}")
        
        # Test with different top_k values
        for top_k in [4, 6, 8, 10]:
            print(f"\n🔍 Testing with top_k={top_k}")
            results = search_similar_images_db(test_image, top_k=top_k, search_type='visual')
            print(f"📊 Results returned: {len(results)}")
            
            for i, result in enumerate(results):
                print(f"  {i+1}. {result['filename']} - similarity: {result['similarity']:.4f}")
                print(f"      House: {result['title']} (ID: {result['house_id']})")
        
        # Check if there are houses without main images
        print(f"\n🔍 Checking houses without main images...")
        cursor.execute("""
            SELECT h.h_id, h.h_title, COUNT(hi.id) as total_images, 
                   SUM(CASE WHEN hi.is_main = 1 THEN 1 ELSE 0 END) as main_images
            FROM house h
            LEFT JOIN house_images hi ON h.h_id = hi.house_id
            GROUP BY h.h_id, h.h_title
            HAVING main_images = 0
            ORDER BY h.h_id
        """)
        
        houses_without_main = cursor.fetchall()
        print(f"📊 Houses without main images: {len(houses_without_main)}")
        for row in houses_without_main:
            house_id, house_title, total_images, main_images = row
            print(f"  House {house_id}: {house_title} - {total_images} images, {main_images} main")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_limited_results()


