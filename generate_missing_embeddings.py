import sqlite3
import os
import numpy as np
import torch
from PIL import Image
import torchvision.models as models
import torchvision.transforms as transforms
from datetime import datetime

# Load pre-trained ResNet18 model (remove last layer)
model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
model = torch.nn.Sequential(*(list(model.children())[:-1]))
model.eval()

# Image transformations
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def extract_feature(image_path):
    """Extract visual features from an image using ResNet18"""
    try:
        image = Image.open(image_path).convert('RGB')
        image = transform(image)
        image = image.unsqueeze(0)
        with torch.no_grad():
            features = model(image)
            features = features.squeeze()
            features = features / torch.norm(features)  # L2 normalization
            return features.numpy()
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def main():
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
    
    if not missing_files:
        print("All images already have embeddings!")
        conn.close()
        return
    
    # Process missing images
    processed_count = 0
    error_count = 0
    
    for i, filename in enumerate(missing_files):
        try:
            image_path = os.path.join(upload_dir, filename)
            print(f"Processing {i+1}/{len(missing_files)}: {filename}")
            
            # Extract features
            features = extract_feature(image_path)
            if features is None:
                error_count += 1
                continue
            
            # Convert features to bytes for database storage
            features_bytes = features.tobytes()
            
            # Insert into database
            cursor.execute("""
                INSERT INTO image_embeddings (image_url, embedding, embedding_type, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                f"uploads/{filename}",
                features_bytes,
                "resnet18_visual",
                datetime.now(),
                datetime.now()
            ))
            
            processed_count += 1
            
            # Commit every 10 images
            if processed_count % 10 == 0:
                conn.commit()
                print(f"  Committed {processed_count} embeddings...")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            error_count += 1
    
    # Final commit
    conn.commit()
    conn.close()
    
    print(f"\nEmbedding generation complete!")
    print(f"  Successfully processed: {processed_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total missing: {len(missing_files)}")

if __name__ == "__main__":
    main()