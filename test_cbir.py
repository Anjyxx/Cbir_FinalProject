#!/usr/bin/env python3
"""
Test CBIR search functionality
"""

from cbir_search import search_similar_images
import os

def test_cbir_search():
    """Test CBIR search with different search types"""
    
    # Test with the first image
    test_image = 'static/uploads/100051498_163247088548284_6174265717089632256_n.jpg_1755597611.png'
    print(f'Testing CBIR search with: {test_image}')
    print(f'File exists: {os.path.exists(test_image)}')
    
    # Test different search types
    for search_type in ['visual', 'style', 'combined']:
        print(f'\n=== Testing {search_type} search ===')
        try:
            results = search_similar_images(test_image, top_k=3, search_type=search_type)
            print(f'Found {len(results)} results')
            for i, result in enumerate(results):
                filename = result.get('filename', 'Unknown')
                similarity = result.get('similarity', 0.0)
                print(f'  {i+1}. {filename} - similarity: {similarity:.4f}')
        except Exception as e:
            print(f'Error in {search_type} search: {e}')
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_cbir_search()
