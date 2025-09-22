import sqlite3
import os

print("Starting debug...")

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

print(f"Embedded filenames: {len(embedded_files)}")

# Find missing embeddings
missing_files = []
for image_file in image_files:
    if image_file not in embedded_files:
        missing_files.append(image_file)

print(f"Images missing embeddings: {len(missing_files)}")

if missing_files:
    print("First 5 missing files:")
    for i, file in enumerate(missing_files[:5]):
        print(f"  {i+1}. {file}")
        
    print("\nFirst 5 embedded files:")
    for i, file in enumerate(embedded_files[:5]):
        print(f"  {i+1}. {file}")

conn.close()
print("Debug complete.")
