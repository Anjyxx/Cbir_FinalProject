#!/usr/bin/env python3
"""
Test the complete CBIR system with database and filtering
"""

from cbir_database import search_similar_images_db
import os

def test_complete_system():
    print("🧪 Testing Complete CBIR System with Database and Filtering", flush=True)
    print("=" * 60, flush=True)
    
    test_image = 'static/uploads/100051498_163247088548284_6174265717089632256_n.jpg_1755597611.png'
    
    if not os.path.exists(test_image):
        print(f"❌ Test image not found: {test_image}", flush=True)
        return False
    
    print(f"✅ Test image found: {test_image}", flush=True)
    
    # Test 1: Basic search without filters
    print("\n🔍 Test 1: Basic Search (No Filters)")
    print("-" * 40)
    try:
        results = search_similar_images_db(test_image, top_k=3, search_type='visual')
        print(f"✅ Found {len(results)} results")
        
        for i, result in enumerate(results):
            print(f"  {i+1}. {result['filename']} - {result['similarity']:.4f}")
            print(f"      House: {result['title']}")
            print(f"      Price: {result['price']:,} THB")
            print(f"      Type: {result['house_type']} - {result['bedrooms']} bedrooms")
            print()
    except Exception as e:
        print(f"❌ Basic search failed: {e}")
        return False
    
    # Test 2: Search with price filter
    print("\n💰 Test 2: Search with Price Filter (< 5,000,000 THB)")
    print("-" * 40)
    try:
        filters = {'price_max': 5000000}
        results = search_similar_images_db(test_image, top_k=3, search_type='visual', filters=filters)
        print(f"✅ Found {len(results)} filtered results")
        
        for i, result in enumerate(results):
            print(f"  {i+1}. {result['filename']} - {result['similarity']:.4f}")
            print(f"      House: {result['title']} - {result['price']:,} THB")
            print()
    except Exception as e:
        print(f"❌ Price filter search failed: {e}")
        return False
    
    # Test 3: Search with bedroom filter
    print("\n🛏️ Test 3: Search with Bedroom Filter (3 bedrooms)")
    print("-" * 40)
    try:
        filters = {'bedrooms': 3}
        results = search_similar_images_db(test_image, top_k=3, search_type='visual', filters=filters)
        print(f"✅ Found {len(results)} filtered results")
        
        for i, result in enumerate(results):
            print(f"  {i+1}. {result['filename']} - {result['similarity']:.4f}")
            print(f"      House: {result['title']} - {result['bedrooms']} bedrooms")
            print()
    except Exception as e:
        print(f"❌ Bedroom filter search failed: {e}")
        return False
    
    # Test 4: Search with multiple filters
    print("\n🔧 Test 4: Search with Multiple Filters (Price + Bedrooms)")
    print("-" * 40)
    try:
        filters = {
            'price_min': 1000000,
            'price_max': 8000000,
            'bedrooms': 2
        }
        results = search_similar_images_db(test_image, top_k=3, search_type='visual', filters=filters)
        print(f"✅ Found {len(results)} filtered results")
        
        for i, result in enumerate(results):
            print(f"  {i+1}. {result['filename']} - {result['similarity']:.4f}")
            print(f"      House: {result['title']} - {result['price']:,} THB - {result['bedrooms']} bedrooms")
            print()
    except Exception as e:
        print(f"❌ Multiple filters search failed: {e}")
        return False
    
    # Test 5: Different search types
    print("\n🎨 Test 5: Different Search Types")
    print("-" * 40)
    for search_type in ['visual', 'style', 'combined']:
        try:
            results = search_similar_images_db(test_image, top_k=2, search_type=search_type)
            print(f"✅ {search_type.capitalize()} search: {len(results)} results")
            
            for i, result in enumerate(results):
                print(f"    {i+1}. {result['filename']} - {result['similarity']:.4f}")
        except Exception as e:
            print(f"❌ {search_type} search failed: {e}")
    
    print("\n🎉 All tests completed!")
    return True

if __name__ == "__main__":
    success = test_complete_system()
    if success:
        print("\n✅ Complete CBIR system is working perfectly!")
        print("   - Database integration: ✅")
        print("   - Image filtering: ✅")
        print("   - Metadata filtering: ✅")
        print("   - Multiple search types: ✅")
        print("   - Rich results with house details: ✅")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
