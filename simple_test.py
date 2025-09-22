#!/usr/bin/env python3
"""
Simple test for CBIR search
"""

from cbir_search import search_similar_images
import os

def main():
    test_image = 'static/uploads/100051498_163247088548284_6174265717089632256_n.jpg_1755597611.png'
    print(f'Testing with: {test_image}')
    print(f'File exists: {os.path.exists(test_image)}')
    
    try:
        results = search_similar_images(test_image, top_k=3, search_type='style')
        print(f'Style search results: {len(results)}')
        for i, result in enumerate(results):
            filename = result.get('filename', 'Unknown')
            similarity = result.get('similarity', 0.0)
            print(f'  {i+1}. {filename} - similarity: {similarity:.4f}')
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


