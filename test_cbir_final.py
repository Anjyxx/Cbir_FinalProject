from cbir_search import search_similar_images
import os

# Test CBIR functionality
test_image = 'static/uploads/100051498_163247088548284_6174265717089632256_n.jpg_1755597611.png'

print(f"Starting CBIR test...")
print(f"Looking for test image: {test_image}")
print(f"Image exists: {os.path.exists(test_image)}")

if os.path.exists(test_image):
    print(f"Testing CBIR with: {test_image}")
    results = search_similar_images(test_image, top_k=5)
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results):
        print(f"  {i+1}. {result['filename']} - similarity: {result['similarity']:.4f}")
else:
    print(f"Test image not found: {test_image}")

# Test with different search types
print("\n" + "="*50)
print("Testing different search types:")

for search_type in ['visual', 'style', 'combined']:
    print(f"\n--- {search_type.upper()} search ---")
    results = search_similar_images(test_image, top_k=3, search_type=search_type)
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results):
        print(f"  {i+1}. {result['filename']} - similarity: {result['similarity']:.4f}")
