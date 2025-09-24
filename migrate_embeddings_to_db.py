import sqlite3
import numpy as np
import os
import sys
sys.path.append('.')

# Import the CBIR search function to get the feature extraction
from cbir_search import extract_feature, should_exclude_image

def migrate_embeddings_to_database():
    """Migrate embeddings from .npy files to the database"""
    
    # Connect to SQLite database
    conn = sqlite3.connect('instance/projectdb.sqlite')
    cursor = conn.cursor()
    
    # Load existing data
    features_file = 'static/features/house_features.npy'
    filenames_file = 'static/features/filenames.npy'
    
    if not os.path.exists(features_file) or not os.path.exists(filenames_file):
        print("Error: Feature files not found")
        return
    
    features = np.load(features_file)
    filenames = np.load(filenames_file)
    
    print(f"Loaded {len(features)} features and {len(filenames)} filenames")
    
    # Get all house images from database
    cursor.execute("""
        SELECT hi.id, hi.house_id, hi.image_url, h.h_title
        FROM house_images hi
        JOIN house h ON hi.house_id = h.h_id
        WHERE h.status = 'active'
        ORDER BY hi.house_id, hi.id
    """)
    db_images = cursor.fetchall()
    
    print(f"Found {len(db_images)} images in database")
    
    # Create a mapping from filename to database info
    filename_to_db = {}
    for img_id, house_id, image_url, house_title in db_images:
        filename = os.path.basename(image_url)
        filename_to_db[filename] = {
            'image_id': img_id,
            'house_id': house_id,
            'image_url': image_url,
            'house_title': house_title
        }
    
    print(f"Created mapping for {len(filename_to_db)} database images")
    
    # Process embeddings
    migrated_count = 0
    skipped_count = 0
    
    for i, (feature, filename) in enumerate(zip(features, filenames)):
        try:
            # Skip excluded images
            if should_exclude_image(filename):
                print(f"Skipping excluded image: {filename}")
                skipped_count += 1
                continue
            
            # Check if this image exists in database
            if filename not in filename_to_db:
                print(f"Image not found in database: {filename}")
                skipped_count += 1
                continue
            
            db_info = filename_to_db[filename]
            
            # Convert numpy array to bytes for storage
            embedding_bytes = feature.tobytes()
            
            # Insert into database
            cursor.execute("""
                INSERT OR REPLACE INTO image_embeddings 
                (image_id, house_id, image_url, embedding, embedding_type)
                VALUES (?, ?, ?, ?, ?)
            """, (
                db_info['image_id'],
                db_info['house_id'],
                db_info['image_url'],
                embedding_bytes,
                'visual'
            ))
            
            migrated_count += 1
            
            if migrated_count % 10 == 0:
                print(f"Migrated {migrated_count} embeddings...")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            skipped_count += 1
    
    # Commit changes
    conn.commit()
    
    # Verify migration
    cursor.execute("SELECT COUNT(*) FROM image_embeddings")
    total_embeddings = cursor.fetchone()[0]
    
    print(f"\nMigration completed!")
    print(f"Migrated: {migrated_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Total embeddings in database: {total_embeddings}")
    
    # Show sample of migrated data
    cursor.execute("""
        SELECT ie.house_id, ie.image_url, h.h_title
        FROM image_embeddings ie
        JOIN house h ON ie.house_id = h.h_id
        LIMIT 5
    """)
    samples = cursor.fetchall()
    print("\nSample migrated embeddings:")
    for house_id, image_url, title in samples:
        print(f"  House {house_id}: {os.path.basename(image_url)} - {title}")
    
    conn.close()

if __name__ == "__main__":
    migrate_embeddings_to_database()



