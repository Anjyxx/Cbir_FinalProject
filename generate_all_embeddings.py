import sqlite3
import numpy as np
import os
import sys
sys.path.append('.')

# Import the CBIR search function to get the feature extraction
from cbir_search import extract_feature, should_exclude_image

def generate_all_embeddings():
    """Generate embeddings for all house images in the database"""
    
    # Connect to SQLite database
    conn = sqlite3.connect('instance/projectdb.sqlite')
    cursor = conn.cursor()
    
    # Get all house images
    cursor.execute("""
        SELECT hi.id, hi.house_id, hi.image_url, h.h_title
        FROM house_images hi
        JOIN house h ON hi.house_id = h.h_id
        WHERE h.status = 'active'
        ORDER BY hi.house_id, hi.id
    """)
    db_images = cursor.fetchall()
    
    print(f"Found {len(db_images)} images in database")
    
    # Clear existing embeddings
    cursor.execute("DELETE FROM image_embeddings")
    print("Cleared existing embeddings")
    
    # Process each image
    processed_count = 0
    skipped_count = 0
    error_count = 0
    
    for i, (img_id, house_id, image_url, house_title) in enumerate(db_images):
        try:
            # Get full image path
            image_path = os.path.join('static', image_url)
            filename = os.path.basename(image_url)
            
            # Check if image file exists
            if not os.path.exists(image_path):
                print(f"Image file not found: {image_path}")
                skipped_count += 1
                continue
            
            # Skip excluded images (floor plans, etc.)
            if should_exclude_image(filename):
                print(f"Skipping excluded image: {filename}")
                skipped_count += 1
                continue
            
            # Extract features
            print(f"Processing {i+1}/{len(db_images)}: {filename}")
            embedding = extract_feature(image_path)
            
            # Convert to bytes
            embedding_bytes = embedding.tobytes()
            
            # Insert into database
            cursor.execute("""
                INSERT INTO image_embeddings 
                (image_id, house_id, image_url, embedding, embedding_type)
                VALUES (?, ?, ?, ?, ?)
            """, (img_id, house_id, image_url, embedding_bytes, 'visual'))
            
            processed_count += 1
            
            # Commit every 10 images
            if processed_count % 10 == 0:
                conn.commit()
                print(f"Processed {processed_count} images...")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            error_count += 1
    
    # Final commit
    conn.commit()
    
    # Verify results
    cursor.execute("SELECT COUNT(*) FROM image_embeddings")
    total_embeddings = cursor.fetchone()[0]
    
    print(f"\nEmbedding generation completed!")
    print(f"Processed: {processed_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")
    print(f"Total embeddings in database: {total_embeddings}")
    
    # Show sample
    cursor.execute("""
        SELECT ie.house_id, ie.image_url, h.h_title
        FROM image_embeddings ie
        JOIN house h ON ie.house_id = h.h_id
        LIMIT 5
    """)
    samples = cursor.fetchall()
    print("\nSample embeddings:")
    for house_id, image_url, title in samples:
        print(f"  House {house_id}: {os.path.basename(image_url)} - {title}")
    
    conn.close()

if __name__ == "__main__":
    generate_all_embeddings()
