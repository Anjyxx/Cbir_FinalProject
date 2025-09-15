import os
import MySQLdb
from pathlib import Path

def check_database_images():
    try:
        # Connect to the database using the same config as the app
        db = MySQLdb.connect(
            host=os.environ.get('MYSQLHOST', 'localhost'),
            user=os.environ.get('MYSQLUSER', 'root'),
            passwd=os.environ.get('MYSQLPASSWORD', ''),
            db=os.environ.get('MYSQLDATABASE', 'projectdb'),
            port=int(os.environ.get('MYSQLPORT', 3307)),
            charset='utf8mb4'
        )
        cursor = db.cursor()
        
        # Get the first 5 houses with their images
        cursor.execute('SELECT h_id, h_title, h_image FROM house LIMIT 5')
        print("\n=== Database Image Paths ===")
        print(f"{'ID':<5} | {'Title':<30} | {'Image Path'}")
        print("-" * 80)
        
        for row in cursor.fetchall():
            house_id, title, image_path = row
            print(f"{house_id:<5} | {title[:30]:<30} | {image_path or 'No image'}")
        
        db.close()
        
    except Exception as e:
        print(f"Error accessing database: {str(e)}")

def check_uploaded_images():
    print("\n=== Checking Uploads Directory ===")
    uploads_dir = Path("static") / "uploads"
    
    if not uploads_dir.exists():
        print(f"Error: Directory not found: {uploads_dir}")
        return
    
    # List first 10 image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    image_files = [f for f in os.listdir(uploads_dir) 
                  if f.lower().endswith(image_extensions)]
    
    print(f"\nFound {len(image_files)} image files in {uploads_dir}")
    print("\nFirst 10 image files:")
    for img in image_files[:10]:
        print(f"- {img}")
    
    # Check if any files are in subdirectories
    print("\nChecking subdirectories...")
    for root, dirs, files in os.walk(uploads_dir):
        if root != str(uploads_dir):  # Skip the root directory we already checked
            rel_path = os.path.relpath(root, uploads_dir)
            img_count = sum(1 for f in files if f.lower().endswith(image_extensions))
            if img_count > 0:
                print(f"- {rel_path}: {img_count} images")

if __name__ == "__main__":
    print("=== Image Path Checker ===")
    check_database_images()
    check_uploaded_images()
