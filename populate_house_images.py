import sqlite3
import os
import time

def populate_house_images():
    """Populate house_images table with files from the uploads directory"""
    
    # Connect to SQLite database
    conn = sqlite3.connect('instance/projectdb.sqlite')
    cursor = conn.cursor()
    
    # Get all active houses
    cursor.execute("SELECT h_id, h_title FROM house WHERE status = 'active'")
    houses = cursor.fetchall()
    print(f"Found {len(houses)} active houses")
    
    # Get all files in uploads directory
    uploads_dir = 'static/uploads'
    if not os.path.exists(uploads_dir):
        print(f"Uploads directory not found: {uploads_dir}")
        return
    
    uploaded_files = [f for f in os.listdir(uploads_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    print(f"Found {len(uploaded_files)} image files in uploads directory")
    
    # Clear existing house_images
    cursor.execute("DELETE FROM house_images")
    print("Cleared existing house_images")
    
    # Assign images to houses (simple round-robin assignment)
    images_per_house = len(uploaded_files) // len(houses) if houses else 0
    print(f"Assigning approximately {images_per_house} images per house")
    
    image_id = 1
    for i, (house_id, house_title) in enumerate(houses):
        # Get images for this house (round-robin)
        start_idx = i * images_per_house
        end_idx = start_idx + images_per_house
        if i == len(houses) - 1:  # Last house gets remaining images
            end_idx = len(uploaded_files)
        
        house_images = uploaded_files[start_idx:end_idx]
        
        print(f"House {house_id} ({house_title}): {len(house_images)} images")
        
        for j, filename in enumerate(house_images):
            # Create image URL
            image_url = f"uploads/{filename}"
            
            # Set first image as main
            is_main = 1 if j == 0 else 0
            
            # Insert into database
            cursor.execute("""
                INSERT INTO house_images (id, house_id, image_url, is_main, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (image_id, house_id, image_url, is_main, time.strftime('%Y-%m-%d %H:%M:%S')))
            
            image_id += 1
    
    # Commit changes
    conn.commit()
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM house_images")
    total_images = cursor.fetchone()[0]
    print(f"Total images inserted: {total_images}")
    
    # Show sample
    cursor.execute("""
        SELECT hi.id, hi.house_id, h.h_title, hi.image_url, hi.is_main
        FROM house_images hi
        JOIN house h ON hi.house_id = h.h_id
        ORDER BY hi.house_id, hi.id
        LIMIT 10
    """)
    samples = cursor.fetchall()
    print("\nSample house_images:")
    for sample in samples:
        print(f"  ID: {sample[0]}, House: {sample[1]} ({sample[2]}), Image: {sample[3]}, Main: {sample[4]}")
    
    conn.close()

if __name__ == "__main__":
    populate_house_images()


