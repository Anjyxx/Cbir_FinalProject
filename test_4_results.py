#!/usr/bin/env python3

import os
from cbir_database import search_similar_images_db

def test_4_results():
    print("Testing CBIR search with 4 results...")
    print("Debug: Function called")
    
    # Get a test image
    uploads_dir = 'static/uploads'
    images = [f for f in os.listdir(uploads_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    if not images:
        print("No images found in uploads directory")
        return
    
    test_img = os.path.join(uploads_dir, images[0])
    print(f"Testing with: {test_img}")
    
    try:
        results = search_similar_images_db(test_img, top_k=4)
        print(f"Found {len(results)} results (expected 4)")
        
        if len(results) == 4:
            print("✅ SUCCESS: CBIR search now returns exactly 4 results!")
        else:
            print(f"⚠️  WARNING: Expected 4 results, got {len(results)}")
        
        # Show the results
        for i, result in enumerate(results):
            print(f"  {i+1}. {result['filename'][:50]}... - {result['similarity']:.4f}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_4_results()
