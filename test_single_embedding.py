import sqlite3
import os
import numpy as np
import torch
from PIL import Image
import torchvision.models as models
import torchvision.transforms as transforms
from datetime import datetime

print("Testing single embedding generation...")

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
        print(f"Processing image: {image_path}")
        image = Image.open(image_path).convert('RGB')
        print(f"Image size: {image.size}")
        
        image = transform(image)
        print(f"Transformed image shape: {image.shape}")
        
        image = image.unsqueeze(0)
        print(f"Batch image shape: {image.shape}")
        
        with torch.no_grad():
            features = model(image)
            print(f"Raw features shape: {features.shape}")
            
            features = features.squeeze()
            print(f"Squeezed features shape: {features.shape}")
            
            features = features / torch.norm(features)  # L2 normalization
            print(f"Normalized features shape: {features.shape}")
            
            return features.numpy()
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        import traceback
        traceback.print_exc()
        return None

# Test with one missing image
upload_dir = 'static/uploads'
test_filename = '1755518128_baan_2.png'
test_path = os.path.join(upload_dir, test_filename)

if os.path.exists(test_path):
    print(f"Testing with: {test_filename}")
    features = extract_feature(test_path)
    
    if features is not None:
        print(f"Success! Features shape: {features.shape}")
        print(f"Features type: {type(features)}")
        print(f"Features dtype: {features.dtype}")
        
        # Test database insertion
        conn = sqlite3.connect('instance/projectdb.sqlite')
        cursor = conn.cursor()
        
        features_bytes = features.tobytes()
        print(f"Features bytes length: {len(features_bytes)}")
        
        cursor.execute("""
            INSERT INTO image_embeddings (image_url, embedding, embedding_type, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            f"uploads/{test_filename}",
            features_bytes,
            "resnet18_visual",
            datetime.now(),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        print("Successfully inserted into database!")
        
    else:
        print("Failed to extract features!")
else:
    print(f"Test image not found: {test_path}")


