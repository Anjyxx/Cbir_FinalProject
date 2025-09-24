import sqlite3
import numpy as np
import os
import sys
sys.path.append('.')

from cbir_search import extract_feature, should_exclude_image

def generate_embeddings_simple():
    """Generate embeddings for all house images - simple version with debug output"""
    
    conn = sqlite3.connect('instance/projectdb.sqlite')
    cursor = conn.cursor()
    
    # Clear existing embeddings
    cursor.execute("DELETE FROM image_embeddings")
    print("Cleared existing embeddings")
    
    # Get all house images
    cursor.execute("""
        SELECT hi.id, hi.house_id, hi.image_url, h.h_title
        FROM house_images hi
        JOIN house h ON hi.house_id = h.h_id
        WHERE h.status = 'active'
        ORDER BY hi.house_id, hi.id
    """)
    db_images = cursor.fetchall()
    
    print(f"Found {len(db_images)} images to process")
    
    processed_count = 0
    skipped_count = 0
    error_count = 0
    
    for i, (img_id, house_id, image_url, house_title) in enumerate(db_images):
        try:
            filename = os.path.basename(image_url)
            image_path = os.path.join('static', image_url)
            
            print(f"Processing {i+1}/{len(db_images)}: House {house_id} - {filename}")
            
            # Check if file exists
            if not os.path.exists(image_path):
                print(f"  -> File not found: {image_path}")
                skipped_count += 1
                continue
            
            # Check if excluded
            if should_exclude_image(filename):
                print(f"  -> Excluded: {filename}")
                skipped_count += 1
                continue
            
            # Extract features
            print(f"  -> Extracting features...")
            embedding = extract_feature(image_path)
            embedding_bytes = embedding.tobytes()
            
            # Insert into database
            cursor.execute("""
                INSERT INTO image_embeddings 
                (image_id, house_id, image_url, embedding, embedding_type)
                VALUES (?, ?, ?, ?, ?)
            """, (img_id, house_id, image_url, embedding_bytes, 'visual'))
            
            processed_count += 1
            print(f"  -> Success! Processed {processed_count} images so far")
            
            # Commit every 5 images
            if processed_count % 5 == 0:
                conn.commit()
                print(f"  -> Committed {processed_count} embeddings")
                
        except Exception as e:
            print(f"  -> ERROR: {e}")
            error_count += 1
    
    # Final commit
    conn.commit()
    
    # Verify results
    cursor.execute("SELECT COUNT(*) FROM image_embeddings")
    total_embeddings = cursor.fetchone()[0]
    
    cursor.execute("SELECT house_id, COUNT(*) FROM image_embeddings GROUP BY house_id")
    by_house = cursor.fetchall()
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Processed: {processed_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")
    print(f"Total embeddings: {total_embeddings}")
    print(f"Embeddings by house:")
    for house_id, count in by_house:
        print(f"  House {house_id}: {count} embeddings")
    
    conn.close()

if __name__ == "__main__":
    generate_embeddings_simple()



