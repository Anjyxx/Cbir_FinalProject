import sqlite3
import os
import numpy as np
import torch
from PIL import Image
import torchvision.models as models
import torchvision.transforms as transforms
from datetime import datetime

# Load pre-trained ResNet18 model (remove last layer)
print("Loading ResNet18 model...")
model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
model = torch.nn.Sequential(*(list(model.children())[:-1]))
model.eval()
print("Model loaded successfully!")

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
    
    # Get all house_images that don't have embeddings yet
    cursor.execute("""
        SELECT hi.id, hi.house_id, hi.image_url 
        FROM house_images hi 
        LEFT JOIN image_embeddings ie ON hi.id = ie.image_id 
        WHERE ie.image_id IS NULL
    """)
    missing_images = cursor.fetchall()
    
    print(f"Found {len(missing_images)} house_images without embeddings")
    
    if not missing_images:
        print("All house_images already have embeddings!")
        conn.close()
        return
    
    # Process missing images
    processed_count = 0
    error_count = 0
    
    for i, (image_id, house_id, image_url) in enumerate(missing_images):
        try:
            # Construct full path to image
            if image_url.startswith('uploads/'):
                image_path = os.path.join('static', image_url)
            else:
                image_path = os.path.join('static/uploads', image_url)
            
            print(f"Processing {i+1}/{len(missing_images)}: {image_url}")
            
            if not os.path.exists(image_path):
                print(f"  Image file not found: {image_path}")
                error_count += 1
                continue
            
            # Extract features
            features = extract_feature(image_path)
            if features is None:
                error_count += 1
                continue
            
            # Convert features to bytes for database storage
            features_bytes = features.tobytes()
            
            # Insert into database
            cursor.execute("""
                INSERT INTO image_embeddings (image_id, house_id, image_url, embedding, embedding_type, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                image_id,
                house_id,
                image_url,
                features_bytes,
                "visual",
                datetime.now(),
                datetime.now()
            ))
            
            processed_count += 1
            
            # Commit every 10 images
            if processed_count % 10 == 0:
                conn.commit()
                print(f"  Committed {processed_count} embeddings...")
                
        except Exception as e:
            print(f"Error processing {image_url}: {e}")
            error_count += 1
    
    # Final commit
    conn.commit()
    conn.close()
    
    print(f"\nEmbedding generation complete!")
    print(f"  Successfully processed: {processed_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total missing: {len(missing_images)}")

if __name__ == "__main__":
    main()
