import sqlite3
import os
import numpy as np

# Connect to database
conn = sqlite3.connect('instance/projectdb.sqlite')
cursor = conn.cursor()

# Get all image files in uploads directory
upload_dir = 'static/uploads'
image_files = [f for f in os.listdir(upload_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
print(f"Total image files in uploads: {len(image_files)}")

# Get all image URLs that have embeddings
cursor.execute("SELECT image_url FROM image_embeddings")
embedded_urls = [row[0] for row in cursor.fetchall()]
print(f"Images with embeddings: {len(embedded_urls)}")

# Extract just the filenames from the URLs (remove 'uploads/' prefix)
embedded_files = []
for url in embedded_urls:
    if url.startswith('uploads/'):
        embedded_files.append(url[8:])  # Remove 'uploads/' prefix
    else:
        embedded_files.append(url)

# Find missing embeddings
missing_files = []
for image_file in image_files:
    if image_file not in embedded_files:
        missing_files.append(image_file)

print(f"Images missing embeddings: {len(missing_files)}")

if missing_files:
    print("\nMissing files:")
    for i, file in enumerate(missing_files[:10]):  # Show first 10
        print(f"  {i+1}. {file}")
    if len(missing_files) > 10:
        print(f"  ... and {len(missing_files) - 10} more")

# Check if we have the feature files
features_file = 'static/features/house_features.npy'
filenames_file = 'static/features/filenames.npy'

print(f"\nFeature files status:")
print(f"  house_features.npy exists: {os.path.exists(features_file)}")
print(f"  filenames.npy exists: {os.path.exists(filenames_file)}")

if os.path.exists(features_file) and os.path.exists(filenames_file):
    features = np.load(features_file)
    filenames = np.load(filenames_file)
    print(f"  Features shape: {features.shape}")
    print(f"  Filenames count: {len(filenames)}")

conn.close()
