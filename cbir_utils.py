#!/usr/bin/env python3
"""
New CBIR System with PyTorch ResNet50
Built alongside existing system for testing and comparison
"""

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import os
import sqlite3
from typing import List, Dict, Optional, Tuple

class NewCBIRSystem:
    """
    New CBIR system with house-level aggregation and metadata scoring
    """
    
    def __init__(self):
        """Initialize the ResNet50 model and transforms"""
        print("🔄 Initializing new CBIR system...")
        
        # Load ResNet50 model (PyTorch version)
        self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        # Remove classification head, keep only feature extraction
        self.model = torch.nn.Sequential(*(list(self.model.children())[:-1]))
        self.model.eval()
        
        # Image transformations
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        print("✅ New CBIR system initialized")
    
    def extract_embedding(self, img_path: str) -> Optional[np.ndarray]:
        """
        Extract L2-normalized feature vector from image
        
        Args:
            img_path: Path to the image file
            
        Returns:
            Normalized embedding vector or None if error
        """
        try:
            if not os.path.exists(img_path):
                print(f"⚠️  Image not found: {img_path}")
                return None
                
            image = Image.open(img_path).convert('RGB')
            image = self.transform(image)
            image = image.unsqueeze(0)
            
            with torch.no_grad():
                features = self.model(image)
                features = features.squeeze()
                # L2 normalization for proper cosine similarity
                features = features / torch.norm(features)
                return features.numpy()
                
        except Exception as e:
            print(f"❌ Error processing {img_path}: {e}")
            return None
    
    def load_house_data_from_db(self) -> List[Dict]:
        """
        Load house data from database with metadata
        
        Returns:
            List of house dictionaries with images and metadata
        """
        print("🔄 Loading house data from database...")
        
        conn = sqlite3.connect('instance/projectdb.sqlite')
        cur = conn.cursor()
        
        # Get all houses with their metadata
        cur.execute("""
            SELECT h.h_id, h.h_title, h.price, h.bedrooms, h.bathrooms, 
                   h.living_area, h.no_of_floors, h.t_id, h.p_id, h.status,
                   t.t_name as type_name, p.p_name as project_name
            FROM house h
            LEFT JOIN house_type t ON h.t_id = t.t_id
            LEFT JOIN project p ON h.p_id = p.p_id
            WHERE h.status = 'active'
            ORDER BY h.h_id
        """)
        
        houses_data = cur.fetchall()
        houses = []
        
        for house_row in houses_data:
            house_id, title, price, bedrooms, bathrooms, area, floors, t_id, p_id, status, type_name, project_name = house_row
            
            # Get all images for this house
            cur.execute("""
                SELECT image_url FROM house_images 
                WHERE house_id = ? AND image_url IS NOT NULL
                ORDER BY is_main DESC, id ASC
            """, (house_id,))
            
            image_rows = cur.fetchall()
            image_paths = []
            
            for img_row in image_rows:
                img_url = img_row[0]
                # Convert to actual file path
                if img_url.startswith('uploads/'):
                    img_path = f"static/{img_url}"
                else:
                    img_path = f"static/uploads/{os.path.basename(img_url)}"
                
                if os.path.exists(img_path):
                    image_paths.append(img_path)
            
            if image_paths:  # Only include houses with valid images
                houses.append({
                    'id': house_id,
                    'title': title,
                    'images': image_paths,
                    'metadata': {
                        'price': float(price) if price else 0,
                        'bedrooms': int(bedrooms) if bedrooms else 0,
                        'bathrooms': float(bathrooms) if bathrooms else 0,
                        'area': float(area) if area else 0,
                        'floors': int(floors) if floors else 0,
                        'type_id': int(t_id) if t_id else 0,
                        'project_id': int(p_id) if p_id else 0,
                        'type_name': type_name or 'Unknown',
                        'project_name': project_name or 'Unknown',
                        'status': status
                    }
                })
        
        conn.close()
        print(f"✅ Loaded {len(houses)} houses with images")
        return houses
    
    def build_embeddings(self, houses: List[Dict], output_file: str = 'house_embeddings_new.npy') -> bool:
        """
        Build embeddings for all house images
        
        Args:
            houses: List of house dictionaries
            output_file: Output file for embeddings
            
        Returns:
            True if successful, False otherwise
        """
        print(f"🔄 Building embeddings for {len(houses)} houses...")
        
        house_data = []
        processed_count = 0
        error_count = 0
        
        for house in houses:
            print(f"Processing house {house['id']}: {house['title']}")
            
            for img_path in house['images']:
                emb = self.extract_embedding(img_path)
                if emb is not None:
                    house_data.append({
                        'house_id': house['id'],
                        'filename': os.path.basename(img_path),
                        'image_path': img_path,
                        'embedding': emb,
                        'metadata': house['metadata']
                    })
                    processed_count += 1
                else:
                    error_count += 1
        
        # Save embeddings
        np.save(output_file, house_data)
        print(f"✅ Saved embeddings for {processed_count} images to {output_file}")
        if error_count > 0:
            print(f"⚠️  Failed to process {error_count} images")
        
        return processed_count > 0
    
    def compute_metadata_score(self, house_metadata: Dict, filters: Optional[Dict] = None) -> float:
        """
        Compute metadata score (0-1) for how well a house matches filters
        
        Args:
            house_metadata: House metadata dictionary
            filters: Optional filters dictionary
            
        Returns:
            Metadata score between 0 and 1
        """
        if not filters:
            return 1.0  # No filtering -> full score
        
        score = 0
        total = len(filters)
        
        for key, value in filters.items():
            if key in house_metadata:
                house_value = house_metadata[key]
                
                # Handle different filter types
                if key.startswith('max_'):
                    # e.g., max_price
                    if isinstance(value, (int, float)) and isinstance(house_value, (int, float)):
                        if house_value <= value:
                            score += 1
                elif key.startswith('min_'):
                    # e.g., min_area
                    if isinstance(value, (int, float)) and isinstance(house_value, (int, float)):
                        if house_value >= value:
                            score += 1
                else:
                    # Exact match
                    if isinstance(value, (int, float)) and isinstance(house_value, (int, float)):
                        if house_value == value:
                            score += 1
                    else:
                        # String comparison (case-insensitive)
                        if str(house_value).lower() == str(value).lower():
                            score += 1
        
        return score / total if total > 0 else 1.0
    
    def search_similar_houses(self, query_image_path: str, top_k: int = 10, 
                            alpha: float = 0.8, filters: Optional[Dict] = None,
                            embeddings_file: str = 'house_embeddings_new.npy') -> List[Dict]:
        """
        Search for similar houses with house-level aggregation
        
        Args:
            query_image_path: Path to query image
            top_k: Number of houses to return
            alpha: Weight for visual similarity (0-1)
            filters: Optional metadata filters
            embeddings_file: Path to embeddings file
            
        Returns:
            List of similar houses with scores
        """
        print(f"🔍 Searching for similar houses...")
        
        # Load embeddings
        if not os.path.exists(embeddings_file):
            print(f"❌ Embeddings file not found: {embeddings_file}")
            return []
        
        house_data = np.load(embeddings_file, allow_pickle=True)
        print(f"📊 Loaded {len(house_data)} image embeddings")
        
        # Extract query embedding
        query_emb = self.extract_embedding(query_image_path)
        if query_emb is None:
            print("❌ Failed to extract query embedding")
            return []
        
        # Compute similarities
        results = []
        for item in house_data:
            # Visual similarity (cosine similarity on normalized embeddings)
            visual_sim = np.dot(query_emb, item['embedding'])
            
            # Metadata score
            metadata_score = self.compute_metadata_score(item['metadata'], filters)
            
            # Combined score
            final_score = alpha * visual_sim + (1 - alpha) * metadata_score
            
            results.append({
                'house_id': item['house_id'],
                'filename': item['filename'],
                'image_path': item['image_path'],
                'visual_similarity': float(visual_sim),
                'metadata_score': float(metadata_score),
                'final_score': float(final_score),
                'metadata': item['metadata']
            })
        
        # Sort by final score
        results.sort(key=lambda x: x['final_score'], reverse=True)
        
        # Aggregate by house_id (keep best image per house)
        best_per_house = {}
        for result in results:
            house_id = result['house_id']
            if house_id not in best_per_house or result['final_score'] > best_per_house[house_id]['final_score']:
                best_per_house[house_id] = result
        
        # Return top-k houses
        top_houses = list(best_per_house.values())[:top_k]
        
        print(f"✅ Found {len(top_houses)} unique houses")
        return top_houses

# Convenience functions for easy usage
def build_new_embeddings():
    """Build embeddings for all houses using the new system"""
    cbir = NewCBIRSystem()
    houses = cbir.load_house_data_from_db()
    return cbir.build_embeddings(houses)

def search_with_new_cbir(query_image_path: str, top_k: int = 10, 
                        alpha: float = 0.8, filters: Optional[Dict] = None):
    """Search using the new CBIR system"""
    cbir = NewCBIRSystem()
    return cbir.search_similar_houses(query_image_path, top_k, alpha, filters)

if __name__ == "__main__":
    # Test the new system
    print("🚀 Testing new CBIR system...")
    
    # Build embeddings
    success = build_new_embeddings()
    if success:
        print("✅ Embeddings built successfully")
        
        # Test search (if we have a test image)
        test_images = [
            'static/uploads/100051498_163247088548284_6174265717089632256_n.jpg_1755597611.png',
            'static/uploads/OIP.jpg'
        ]
        
        for test_img in test_images:
            if os.path.exists(test_img):
                print(f"\n🔍 Testing search with: {test_img}")
                results = search_with_new_cbir(test_img, top_k=5)
                
                print(f"Found {len(results)} results:")
                for i, result in enumerate(results, 1):
                    print(f"  {i}. House {result['house_id']} - Score: {result['final_score']:.4f} "
                          f"(Visual: {result['visual_similarity']:.4f}, Metadata: {result['metadata_score']:.4f})")
                break
    else:
        print("❌ Failed to build embeddings")
