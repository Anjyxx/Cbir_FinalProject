#!/usr/bin/env python3
"""
Simple test for CBIR filtering
"""

from cbir_search import search_similar_images, should_exclude_image

def test_filtering():
    print("Testing image filtering...")
    
    # Test specific filenames
    test_cases = [
        ('1755602325_LINE_ALBUM____12_2.png', True),  # Should be excluded
        ('house_photo.jpg', False),  # Should be included
        ('floor_plan.png', True),  # Should be excluded
        ('site_plan.jpg', True),  # Should be excluded
        ('baan_1.png', False),  # Should be included
    ]
    
    for filename, should_exclude in test_cases:
        result = should_exclude_image(filename)
        status = "✓" if result == should_exclude else "✗"
        print(f"{status} {filename}: {'EXCLUDED' if result else 'INCLUDED'} (expected: {'EXCLUDED' if should_exclude else 'INCLUDED'})")

def test_cbir():
    print("\nTesting CBIR search...")
    test_image = 'static/uploads/100051498_163247088548284_6174265717089632256_n.jpg_1755597611.png'
    
    try:
        results = search_similar_images(test_image, top_k=5, search_type='visual')
        print(f"Found {len(results)} results:")
        
        for i, result in enumerate(results):
            filename = result['filename']
            similarity = result['similarity']
            print(f"  {i+1}. {filename} - {similarity:.4f}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_filtering()
    test_cbir()
