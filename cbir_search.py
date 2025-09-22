import numpy as np
import torch
from PIL import Image
import torchvision.models as models
import torchvision.transforms as transforms
import os

# Paths
FEATURES_FILE = 'static/features/house_features.npy'
FILENAMES_FILE = 'static/features/filenames.npy'
STYLE_FEATURES_FILE = 'static/features/house_style_features.npy'

# Load pre-trained ResNet18 model (remove last layer)
model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
model = torch.nn.Sequential(*(list(model.children())[:-1]))
model.eval()

# Load pre-trained ResNet50 model for style features (produces 2048 dimensions)
style_model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
style_model = torch.nn.Sequential(*(list(style_model.children())[:-1]))
style_model.eval()

# Image transformations
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def extract_feature(image_path):
    """Extract visual features from an image using ResNet18"""
    image = Image.open(image_path).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)
    with torch.no_grad():
        features = model(image)
        features = features.squeeze()
        features = features / torch.norm(features)  # L2 normalization
        return features.numpy()

def extract_style_feature(image_path):
    """Extract style features from an image using ResNet50 (2048 dimensions)"""
    image = Image.open(image_path).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)
    with torch.no_grad():
        features = style_model(image)
        features = features.squeeze()
        features = features / torch.norm(features)  # L2 normalization
        return features.numpy()

def should_exclude_image(filename):
    """
    Determine if an image should be excluded from CBIR results.
    Excludes floor plans, blueprints, architectural drawings, and other non-photographic images.
    """
    if not filename:
        return True
    
    filename_lower = filename.lower()
    
    # Keywords that indicate non-photographic images
    exclude_keywords = [
        'plan', 'blueprint', 'drawing', 'sketch', 'diagram', 'layout',
        'floor_plan', 'site_plan', 'architectural', 'design', 'blueprint',
        'line_album', 'album', 'chart', 'graph', 'map', 'schematic',
        'technical', 'engineering', 'construction', 'detail', 'section',
        'elevation', 'perspective', 'rendering', '3d', 'cad', 'dwg',
        'siteplan', 'floorplan', 'house_plan', 'house1_plan', 'house2_plan',
        'baan_', 'inside_', 'cover', 'cover2', 'sale_', 'sale3'
    ]
    
    # Check if filename contains any exclude keywords
    for keyword in exclude_keywords:
        if keyword in filename_lower:
            return True
    
    # Additional patterns to exclude
    exclude_patterns = [
        'line_album',  # LINE album images are often floor plans
        'site_plan',   # Site plans
        'floor_plan',  # Floor plans
        'plan_',       # Any plan images
        '_plan',       # Any plan images
        'blueprint',   # Blueprints
        'drawing',     # Drawings
        'diagram',     # Diagrams
        'siteplan',    # Site plan variations
        'floorplan',   # Floor plan variations
        'house1_plan', # Specific house plan patterns
        'house2_plan',
        'house_plan',
        'baan_',       # Thai house plan patterns
        'inside_',     # Interior plans
        'cover',       # Cover images (often plans)
        'sale_',       # Sale images (often plans)
    ]
    
    for pattern in exclude_patterns:
        if pattern in filename_lower:
            return True
    
    # Check for specific problematic patterns
    problematic_patterns = [
        'line_album____',  # LINE album patterns
        'siteplan_',       # Site plan patterns
        'house1_plan',     # House plan patterns
        'baan_4s_type',    # Thai house type patterns
        'inside_s',        # Interior plan patterns
    ]
    
    for pattern in problematic_patterns:
        if pattern in filename_lower:
            return True
    
    return False

def search_similar_images(query_image_path, top_k=6, search_type='visual'):
    """
    Search for similar images based on different criteria
    
    Args:
        query_image_path: Path to the query image
        top_k: Number of similar images to return
        search_type: Type of search ('visual', 'style', 'combined')
    
    Returns:
        List of dictionaries with filename and similarity score
    """
    try:
        # Extract features for the query image based on search type
        if search_type == 'visual':
            query_feat = extract_feature(query_image_path)
            features_file = FEATURES_FILE
        elif search_type == 'style':
            query_feat = extract_style_feature(query_image_path)
            features_file = STYLE_FEATURES_FILE
        elif search_type == 'combined':
            # For combined search, we'll use visual features as primary
            query_feat = extract_feature(query_image_path)
            features_file = FEATURES_FILE
        else:
            raise ValueError(f"Unknown search type: {search_type}")

        # Load database features and filenames
        if not os.path.exists(features_file):
            print(f"Warning: Features file {features_file} not found. Using visual features as fallback.")
            features_file = FEATURES_FILE
            query_feat = extract_feature(query_image_path)
        
        db_features = np.load(features_file)
        db_filenames = np.load(FILENAMES_FILE)
        
        # Ensure arrays have matching lengths (use minimum length)
        min_length = min(len(db_filenames), len(db_features))
        if len(db_filenames) != len(db_features):
            print(f"Warning: Filenames ({len(db_filenames)}) and features ({len(db_features)}) have different lengths. Using first {min_length} items.")
            db_filenames = db_filenames[:min_length]
            db_features = db_features[:min_length]

        # Compute cosine similarity
        similarities = np.dot(db_features, query_feat) / (
            np.linalg.norm(db_features, axis=1) * np.linalg.norm(query_feat) + 1e-10
        )

        # For combined search, we can enhance with style features if available
        if search_type == 'combined' and os.path.exists(STYLE_FEATURES_FILE):
            try:
                style_features = np.load(STYLE_FEATURES_FILE)
                style_query_feat = extract_style_feature(query_image_path)
                
                # Ensure style features have the same length as visual features
                min_style_length = min(len(style_features), len(db_features))
                style_features = style_features[:min_style_length]
                
                style_similarities = np.dot(style_features, style_query_feat) / (
                    np.linalg.norm(style_features, axis=1) * np.linalg.norm(style_query_feat) + 1e-10
                )
                
                # Ensure both similarity arrays have the same length
                min_sim_length = min(len(similarities), len(style_similarities))
                similarities = similarities[:min_sim_length]
                style_similarities = style_similarities[:min_sim_length]
                
                # Combine visual and style similarities (weighted average)
                similarities = 0.7 * similarities + 0.3 * style_similarities
            except Exception as e:
                print(f"Warning: Could not load style features for combined search: {e}")

        # Get all indices sorted by similarity (descending)
        all_indices = np.argsort(similarities)[::-1]
        
        results = []
        for idx in all_indices:
            filename = db_filenames[idx]
            
            # Filter out non-photographic images (floor plans, blueprints, etc.)
            if should_exclude_image(filename):
                continue
                
            results.append({
                'filename': filename,
                'similarity': float(similarities[idx])
            })
            
            # Stop when we have enough results
            if len(results) >= top_k:
                break
        
        return results
        
    except Exception as e:
        print(f"Error in CBIR search: {e}")
        import traceback
        traceback.print_exc()
        return []

def create_style_features():
    """
    Create style features for all images in the database
    This function can be called to generate style features if they don't exist
    """
    if not os.path.exists(FILENAMES_FILE):
        print("Error: Filenames file not found. Please run feature extraction first.")
        return
    
    filenames = np.load(FILENAMES_FILE)
    style_features = []
    
    print(f"Creating style features for {len(filenames)} images...")
    
    for i, filename in enumerate(filenames):
        try:
            image_path = os.path.join('static/uploads', filename)
            if os.path.exists(image_path):
                style_feat = extract_style_feature(image_path)
                style_features.append(style_feat)
                if (i + 1) % 10 == 0:
                    print(f"Processed {i + 1}/{len(filenames)} images...")
            else:
                print(f"Warning: Image not found: {image_path}")
                # Add zero vector as placeholder
                style_features.append(np.zeros(2048))  # ResNet50 feature size
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            # Add zero vector as placeholder
            style_features.append(np.zeros(2048))
    
    # Save style features
    np.save(STYLE_FEATURES_FILE, np.array(style_features))
    print(f"Style features saved to {STYLE_FEATURES_FILE}")

if __name__ == "__main__":
    # Test the enhanced functionality
    test_image = 'static/uploads/100051498_163247088548284_6174265717089632256_n.jpg_1755597611.png'
    if os.path.exists(test_image):
        print("Testing enhanced CBIR functionality...")
        for search_type in ['visual', 'style', 'combined']:
            print(f"\n=== Testing {search_type} search ===")
            results = search_similar_images(test_image, top_k=3, search_type=search_type)
            print(f"Found {len(results)} results")
            for i, result in enumerate(results):
                print(f"  {i+1}. {result['filename']} - similarity: {result['similarity']:.4f}")
    else:
        print("Test image not found. Please check the path.") 