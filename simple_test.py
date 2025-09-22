#!/usr/bin/env python3
"""
Simple CBIR system test
"""

import sys
from cbir_database import search_similar_images_db
import os

def main():
    print("🧪 Testing CBIR System", flush=True)
    print("=" * 40, flush=True)
    
    test_image = 'static/uploads/100051498_163247088548284_6174265717089632256_n.jpg_1755597611.png'
    
    if not os.path.exists(test_image):
        print(f"❌ Test image not found: {test_image}", flush=True)
        return False
    
    print(f"✅ Test image found: {test_image}", flush=True)
    
    # Test 1: Basic search
    print("\n🔍 Test 1: Basic Search", flush=True)
    try:
        results = search_similar_images_db(test_image, top_k=3, search_type='visual')
        print(f"✅ Found {len(results)} results", flush=True)
        
        for i, result in enumerate(results):
            print(f"  {i+1}. {result['filename']} - {result['similarity']:.4f}", flush=True)
            print(f"      House: {result['title']}", flush=True)
            print(f"      Price: {result['price']:,} THB", flush=True)
            print(f"      Type: {result['house_type']} - {result['bedrooms']} bedrooms", flush=True)
            print()
    except Exception as e:
        print(f"❌ Basic search failed: {e}", flush=True)
        return False
    
    # Test 2: Search with price filter
    print("\n💰 Test 2: Price Filter (< 5,000,000 THB)", flush=True)
    try:
        filters = {'price_max': 5000000}
        results = search_similar_images_db(test_image, top_k=3, search_type='visual', filters=filters)
        print(f"✅ Found {len(results)} filtered results", flush=True)
        
        for i, result in enumerate(results):
            print(f"  {i+1}. {result['filename']} - {result['similarity']:.4f}", flush=True)
            print(f"      House: {result['title']} - {result['price']:,} THB", flush=True)
            print()
    except Exception as e:
        print(f"❌ Price filter search failed: {e}", flush=True)
        return False
    
    print("\n🎉 All tests completed successfully!", flush=True)
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ CBIR system is working perfectly!", flush=True)
    else:
        print("\n❌ Some tests failed.", flush=True)
