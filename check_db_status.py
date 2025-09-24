import sqlite3

# Connect to database
conn = sqlite3.connect('instance/projectdb.sqlite')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Available tables:")
for table in tables:
    print(f"  - {table[0]}")

# Check image_embeddings count
try:
    cursor.execute("SELECT COUNT(*) FROM image_embeddings")
    count = cursor.fetchone()[0]
    print(f"\nImage embeddings count: {count}")
except Exception as e:
    print(f"Error checking image_embeddings: {e}")

# Check if we have any image files
import os
upload_dir = 'static/uploads'
if os.path.exists(upload_dir):
    image_files = [f for f in os.listdir(upload_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    print(f"\nImage files in uploads: {len(image_files)}")
    if len(image_files) > 0:
        print("Sample files:")
        for i, file in enumerate(image_files[:5]):
            print(f"  - {file}")
        if len(image_files) > 5:
            print(f"  ... and {len(image_files) - 5} more")
else:
    print("\nUploads directory not found")

conn.close()



