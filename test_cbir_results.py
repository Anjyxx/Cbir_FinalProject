#!/usr/bin/env python3

import os
import sys
import numpy as np

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_cbir_results():
    print("🔍 Testing CBIR results in detail...")
    
    try:
        from cbir_database import search_similar_images_db
        
        # Test with a sample image
        test_image = 'static/uploads/OIP_4.webp'  # Using the image from the logs
        
        if not os.path.exists(test_image):
            print(f"❌ Test image not found: {test_image}")
            # Try to find any image in uploads
            upload_dir = 'static/uploads'
            if os.path.exists(upload_dir):
                images = [f for f in os.listdir(upload_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
                if images:
                    test_image = os.path.join(upload_dir, images[0])
                    print(f"📷 Using test image: {test_image}")
                else:
                    print("❌ No images found in uploads directory")
                    return
            else:
                print("❌ Uploads directory not found")
                return
        
        print(f"📷 Testing with image: {test_image}")
        
        # Test with different top_k values
        for top_k in [2, 4, 6, 10]:
            print(f"\n🔍 Testing with top_k={top_k}")
            results = search_similar_images_db(test_image, top_k=top_k, search_type='visual')
            print(f"📊 Results returned: {len(results)}")
            
            for i, result in enumerate(results):
                print(f"  {i+1}. {result['filename']} - similarity: {result['similarity']:.4f}")
                print(f"      House: {result['title']} (ID: {result['house_id']})")
        
        # Test with style search
        print(f"\n🎨 Testing style search with top_k=4")
        style_results = search_similar_images_db(test_image, top_k=4, search_type='style')
        print(f"📊 Style results returned: {len(style_results)}")
        
        for i, result in enumerate(style_results):
            print(f"  {i+1}. {result['filename']} - similarity: {result['similarity']:.4f}")
            print(f"      House: {result['title']} (ID: {result['house_id']})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cbir_results()



