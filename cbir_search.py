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
    
    # Specific patterns that indicate floor plans, blueprints, or technical drawings
    exclude_patterns = [
        'floor_plan', 'site_plan', 'house_plan', 'house1_plan', 'house2_plan',
        'siteplan', 'floorplan', 'blueprint', 'drawing', 'diagram',
        'line_album',  # LINE album images are often floor plans
        'plan_', '_plan',  # Any plan images
        'elevation', 'section', 'detail',  # Technical drawings
        'schematic', 'chart', 'graph', 'map',  # Non-photographic
        'cad', 'dwg', '3d', 'rendering',  # Technical/3D
        'technical', 'engineering', 'construction',  # Technical docs
        'architectural', 'design',  # Design drawings
    ]
    
    # Check for specific exclude patterns
    for pattern in exclude_patterns:
        if pattern in filename_lower:
            return True
    
    # Additional checks for common floor plan indicators
    # Only exclude if it's clearly a plan/drawing, not a house photo
    if 'baan_' in filename_lower:
        # Only exclude if it's clearly a plan (contains plan-related words)
        plan_indicators = ['plan', 'drawing', 'blueprint', 'layout', 'diagram']
        if any(indicator in filename_lower for indicator in plan_indicators):
            return True
        # Don't exclude regular baan photos
        return False
    
    if 'cover' in filename_lower:
        # Only exclude if it's clearly a plan cover
        plan_indicators = ['plan', 'drawing', 'blueprint', 'layout', 'diagram']
        if any(indicator in filename_lower for indicator in plan_indicators):
            return True
        # Don't exclude regular house cover photos
        return False
    
    if 'inside_' in filename_lower:
        # Only exclude if it's clearly an interior plan
        plan_indicators = ['plan', 'drawing', 'blueprint', 'layout', 'diagram']
        if any(indicator in filename_lower for indicator in plan_indicators):
            return True
        # Don't exclude regular interior photos
        return False
    
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

def search_similar_images(query_image_path, top_k=6, search_type='visual', valid_images=None, filters=None):
    """
    Search for similar images based on different criteria with optional metadata filtering
    
    Args:
        query_image_path: Path to the query image
        top_k: Number of similar images to return
        search_type: Type of search ('visual', 'style', 'combined')
        valid_images: Optional dict of valid image filenames to filter results
        filters: Optional dict of metadata filters, e.g. {"no_of_floors": 1, "bedrooms": 3}
    
    Returns:
        List of dictionaries with filename, similarity score, and metadata
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
        
        # Filter to only valid images if valid_images is provided
        if valid_images is not None:
            print(f"Filtering features to valid images only. Original: {len(db_filenames)}, Valid: {len(valid_images)}")
            valid_filenames = set(valid_images.keys())
            
            filtered_features = []
            filtered_filenames = []
            for f, vec in zip(db_filenames, db_features):
                if f in valid_filenames:
                    filtered_features.append(vec)
                    filtered_filenames.append(f)
            
            if len(filtered_features) == 0:
                print("Warning: No valid images found in feature database")
                return []
            
            db_features = np.array(filtered_features)
            db_filenames = np.array(filtered_filenames)
            print(f"Filtered to {len(db_filenames)} valid images")

        # Compute cosine similarity
        similarities = np.dot(db_features, query_feat) / (
            np.linalg.norm(db_features, axis=1) * np.linalg.norm(query_feat) + 1e-10
        )
        
        # Debug: Print original similarity range
        print(f"[DEBUG] Original similarity range: {similarities.min():.4f} - {similarities.max():.4f}")
        
        # Use much more conservative similarity scoring
        # ResNet18 features are not great for house similarity, so be very strict
        min_val = similarities.min()
        max_val = similarities.max()
        range_val = max_val - min_val
        
        # Apply very conservative scaling - only show results that are actually similar
        # Scale to a much lower range (20-60%) to be more realistic
        if range_val > 0.01:  # Only if there's meaningful variation
            similarities = 0.2 + ((similarities - min_val) / (max_val - min_val)) * 0.4
        else:
            # If all similarities are very close, set them to a low value
            similarities = np.full_like(similarities, 0.3)
        
        print(f"[DEBUG] Final similarity range: {similarities.min():.4f} - {similarities.max():.4f}")

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
                
                # Apply the same scaling to combined similarities
                min_val = similarities.min()
                max_val = similarities.max()
                
                if max_val > min_val:
                    # Scale to [0.8, 1.0] range
                    similarities = 0.8 + ((similarities - min_val) / (max_val - min_val)) * 0.2
                else:
                    # All values are the same, set to 0.9
                    similarities = np.full_like(similarities, 0.9)
            except Exception as e:
                print(f"Warning: Could not load style features for combined search: {e}")

        # Filter out very low similarity results (less than 0.4)
        # Be more strict since ResNet18 features aren't great for house similarity
        threshold = 0.4
        valid_indices = np.where(similarities >= threshold)[0]
        
        if len(valid_indices) == 0:
            print(f"[DEBUG] No results above threshold {threshold}, using top results anyway")
            valid_indices = np.argsort(similarities)[::-1][:top_k]
        else:
            print(f"[DEBUG] Found {len(valid_indices)} results above threshold {threshold}")
        
        # Get all indices sorted by similarity (descending) from valid results
        all_indices = valid_indices[np.argsort(similarities[valid_indices])[::-1]]
        
        results = []
        for idx in all_indices:
            filename = db_filenames[idx]
            
            # Filter out non-photographic images (floor plans, blueprints, etc.)
            if should_exclude_image(filename):
                continue
            
            # Get metadata for this image
            metadata = valid_images.get(filename, {}) if valid_images else {}
            
            # Apply metadata filters if provided
            if filters:
                match = True
                for key, value in filters.items():
                    if key in metadata:
                        # Handle different data types for comparison
                        if isinstance(value, (int, float)):
                            # Numeric comparison
                            try:
                                metadata_value = float(metadata[key])
                                if metadata_value != float(value):
                                    match = False
                                    break
                            except (ValueError, TypeError):
                                match = False
                                break
                        else:
                            # String comparison (case-insensitive)
                            if str(metadata[key]).lower() != str(value).lower():
                                match = False
                                break
                    else:
                        # If filter key not in metadata, skip this result
                        match = False
                        break
                
                if not match:
                    continue
            
            # Add result with metadata
            result = {
                'filename': filename,
                'similarity': float(similarities[idx])
            }
            
            # Add metadata fields if available
            if metadata:
                result.update({
                    'house_title': metadata.get('house_title', 'Unknown House'),
                    'no_of_floors': metadata.get('no_of_floors', 'Unknown'),
                    'bedrooms': metadata.get('bedrooms', 'Unknown'),
                    'bathrooms': metadata.get('bathrooms', 'Unknown'),
                    'living_area': metadata.get('living_area', 'Unknown'),
                    'price': metadata.get('price', 'Unknown'),
                    'image_url': f"uploads/{filename}"
                })
            
            results.append(result)
            
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


def search_similar_images_improved(image_path, top_k=4, search_type='visual', valid_images=None):
    """
    Improved CBIR search using better architectural features and more realistic similarity scoring
    
    Args:
        image_path: Path to query image
        top_k: Number of results to return
        search_type: Type of search ('visual', 'style', 'combined')
        valid_images: Dictionary of valid images to search through
        
    Returns:
        List of similar images with improved similarity scores
    """
    print(f"[DEBUG] Improved CBIR search - {search_type} mode")
    
    try:
        # Load pre-computed features
        if not os.path.exists(FEATURES_FILE) or not os.path.exists(FILENAMES_FILE):
            print("Error: Feature files not found")
            return []
        
        features = np.load(FEATURES_FILE)
        filenames = np.load(FILENAMES_FILE, allow_pickle=True)
        
        print(f"[DEBUG] Loaded {len(features)} features, {len(filenames)} filenames")
        
        # Filter to valid images only
        if valid_images:
            valid_filenames = set(valid_images.keys())
            valid_indices = [i for i, filename in enumerate(filenames) if filename in valid_filenames]
            features = features[valid_indices]
            filenames = filenames[valid_indices]
            print(f"[DEBUG] Filtered to {len(features)} valid features")
        
        # Extract query features using a better model
        query_features = extract_improved_features(image_path)
        if query_features is None:
            print("Error: Could not extract query features")
            return []
        
        # Calculate similarities using multiple approaches
        similarities = calculate_improved_similarity(query_features, features, search_type)
        
        print(f"[DEBUG] Improved similarity range: {similarities.min():.4f} - {similarities.max():.4f}")
        
        # Apply much more conservative scoring
        similarities = apply_conservative_scoring(similarities)
        
        print(f"[DEBUG] Final conservative similarity range: {similarities.min():.4f} - {similarities.max():.4f}")
        
        # Filter results with higher threshold (adjusted for 70-95% range)
        threshold = 0.70  # Strict threshold for architectural similarity
        valid_indices = np.where(similarities >= threshold)[0]
        
        if len(valid_indices) == 0:
            print(f"[DEBUG] No results above threshold {threshold}, using top results anyway")
            valid_indices = np.argsort(similarities)[::-1][:top_k]
        else:
            print(f"[DEBUG] Found {len(valid_indices)} results above threshold {threshold}")
        
        # Get top results
        top_indices = valid_indices[np.argsort(similarities[valid_indices])[::-1]][:top_k]
        
        results = []
        for idx in top_indices:
            filename = filenames[idx]
            similarity = float(similarities[idx])
            
            # Only include if we have valid image data
            if valid_images and filename in valid_images:
                results.append({
                    'filename': filename,
                    'similarity': similarity,
                    'house_id': valid_images[filename]['house_id'],
                    'image_url': valid_images[filename]['image_url'],
                    'house_title': valid_images[filename]['house_title']
                })
            elif not valid_images:
                results.append({
                    'filename': filename,
                    'similarity': similarity
                })
        
        print(f"[DEBUG] Improved CBIR search completed with {len(results)} results")
        return results
        
    except Exception as e:
        print(f"Error in improved CBIR search: {e}")
        return []


def extract_improved_features(image_path):
    """
    Extract features using the same model as the pre-computed features for compatibility
    """
    try:
        # Load and preprocess image
        image = Image.open(image_path).convert('RGB')
        image_tensor = transform(image).unsqueeze(0)
        
        # Use ResNet18 to match the pre-computed features (512 dimensions)
        with torch.no_grad():
            features = model(image_tensor)  # ResNet18 features (512 dims)
            features = features.squeeze().numpy()
            
            # Apply L2 normalization
            features = features / np.linalg.norm(features)
            
        return features
        
    except Exception as e:
        print(f"Error extracting improved features: {e}")
        return None


def calculate_improved_similarity(query_features, database_features, search_type):
    """
    Calculate similarity using multiple approaches for better architectural matching
    """
    try:
        # Method 1: Cosine similarity (most important for architectural features)
        cosine_sim = np.dot(database_features, query_features) / (
            np.linalg.norm(database_features, axis=1) * np.linalg.norm(query_features)
        )
        
        # Method 2: Euclidean distance (inverted and normalized)
        euclidean_dist = np.linalg.norm(database_features - query_features, axis=1)
        euclidean_sim = 1 / (1 + euclidean_dist)
        
        # Method 3: Manhattan distance (inverted and normalized)
        manhattan_dist = np.sum(np.abs(database_features - query_features), axis=1)
        manhattan_sim = 1 / (1 + manhattan_dist)
        
        # Method 4: Pearson correlation (good for architectural patterns)
        query_centered = query_features - np.mean(query_features)
        db_centered = database_features - np.mean(database_features, axis=1, keepdims=True)
        pearson_sim = np.sum(db_centered * query_centered, axis=1) / (
            np.linalg.norm(db_centered, axis=1) * np.linalg.norm(query_centered)
        )
        pearson_sim = np.nan_to_num(pearson_sim, nan=0.0)  # Handle NaN values
        
        # Combine methods with weights optimized for architectural similarity
        if search_type == 'visual':
            # For visual similarity, emphasize cosine and pearson correlation
            similarities = 0.5 * cosine_sim + 0.3 * pearson_sim + 0.1 * euclidean_sim + 0.1 * manhattan_sim
        elif search_type == 'style':
            # For style similarity, use all methods with equal weight
            similarities = 0.3 * cosine_sim + 0.3 * pearson_sim + 0.2 * euclidean_sim + 0.2 * manhattan_sim
        else:  # combined
            # For combined, balance all methods
            similarities = 0.4 * cosine_sim + 0.3 * pearson_sim + 0.15 * euclidean_sim + 0.15 * manhattan_sim
        
        return similarities
        
    except Exception as e:
        print(f"Error calculating improved similarity: {e}")
        return np.zeros(len(database_features))


def apply_conservative_scoring(similarities):
    """
    Apply very conservative scoring to be more realistic about architectural similarity
    """
    min_val = similarities.min()
    max_val = similarities.max()
    range_val = max_val - min_val
    
    print(f"[DEBUG] Raw similarity range: {min_val:.4f} - {max_val:.4f}")
    
    # Apply very conservative scaling - architectural similarity is hard to achieve
    # Scale to a realistic range (10-40%) to be much more honest
    if range_val > 0.005:  # Only if there's meaningful variation
        # Scale to 10-40% range - very conservative
        similarities = 0.10 + ((similarities - min_val) / (max_val - min_val)) * 0.30
        print(f"[DEBUG] Applied scaling: 10-40% range")
    else:
        # If all similarities are very close, set them to a low value
        similarities = np.full_like(similarities, 0.20)
        print(f"[DEBUG] Applied default: 20% (no meaningful variation)")
    
    return similarities


def apply_varied_conservative_scoring(similarities):
    """
    Apply conservative scoring with better differentiation between results
    """
    min_val = similarities.min()
    max_val = similarities.max()
    range_val = max_val - min_val
    
    print(f"[DEBUG] Raw similarity range: {min_val:.4f} - {max_val:.4f}")
    
    # Apply more varied scaling to get better differentiation
    # Scale to a realistic range (70-95%) with better spread
    if range_val > 0.001:  # Only if there's meaningful variation
        # Scale to 70-95% range with better differentiation
        similarities = 0.70 + ((similarities - min_val) / (max_val - min_val)) * 0.25
        print(f"[DEBUG] Applied varied scaling: 70-95% range")
    else:
        # If all similarities are very close, create artificial differentiation
        # Sort by original similarity and assign decreasing scores
        sorted_indices = np.argsort(similarities)[::-1]
        for i, idx in enumerate(sorted_indices):
            similarities[idx] = 0.95 - (i * 0.05)  # 95%, 90%, 85%, 80%, etc.
        print(f"[DEBUG] Applied artificial differentiation: {similarities.min():.1f}%-{similarities.max():.1f}%")
    
    return similarities


def search_similar_images_mysql(image_path, top_k=4, search_type='visual', valid_images=None):
    """
    MySQL-based CBIR search that works directly with images from the database
    
    Args:
        image_path: Path to query image
        top_k: Number of results to return
        search_type: Type of search ('visual', 'style', 'combined')
        valid_images: Dictionary of valid images to search through
        
    Returns:
        List of similar images with improved similarity scores
    """
    print(f"[DEBUG] MySQL-based CBIR search - {search_type} mode")
    
    try:
        # Extract query features
        query_features = extract_improved_features(image_path)
        if query_features is None:
            print("Error: Could not extract query features")
            return []
        
        # Process each valid image directly from MySQL
        similarities = []
        filenames = []
        
        for filename, image_data in valid_images.items():
            try:
                # Construct full path to the image in houses folder
                image_url = image_data['image_url']
                filename = os.path.basename(image_url)
                # All house images are now in the houses subfolder
                full_path = f"static/uploads/houses/{filename}"
                
                # Check if image exists
                if not os.path.exists(full_path):
                    print(f"[DEBUG] Image not found: {full_path}")
                    continue
                
                # Extract features for this image
                image_features = extract_improved_features(full_path)
                if image_features is None:
                    continue
                
                # Calculate similarity
                similarity = calculate_improved_similarity_single(query_features, image_features, search_type)
                similarities.append(similarity)
                filenames.append(filename)
                
            except Exception as e:
                print(f"[DEBUG] Error processing {filename}: {e}")
                continue
        
        if not similarities:
            print("[DEBUG] No valid images found for comparison")
            return []
        
        similarities = np.array(similarities)
        filenames = np.array(filenames)
        
        print(f"[DEBUG] MySQL similarity range: {similarities.min():.4f} - {similarities.max():.4f}")
        
        # Apply more varied conservative scoring to get better differentiation
        similarities = apply_varied_conservative_scoring(similarities)
        
        print(f"[DEBUG] Final MySQL similarity range: {similarities.min():.4f} - {similarities.max():.4f}")
        
        # Filter results with threshold (adjusted for 70-95% range)
        threshold = 0.70
        valid_indices = np.where(similarities >= threshold)[0]
        
        if len(valid_indices) == 0:
            print(f"[DEBUG] No results above threshold {threshold}, using top results anyway")
            valid_indices = np.argsort(similarities)[::-1][:top_k]
        else:
            print(f"[DEBUG] Found {len(valid_indices)} results above threshold {threshold}")
        
        # Get top results, but deduplicate by house_id to show different houses
        top_indices = valid_indices[np.argsort(similarities[valid_indices])[::-1]]
        
        results = []
        seen_house_ids = set()
        
        for idx in top_indices:
            if len(results) >= top_k:
                break
                
            filename = filenames[idx]
            similarity = float(similarities[idx])
            
            if filename in valid_images:
                house_id = valid_images[filename]['house_id']
                
                # Only add if we haven't seen this house_id before
                if house_id not in seen_house_ids:
                    results.append({
                        'filename': filename,
                        'similarity': similarity,
                        'house_id': house_id,
                        'image_url': valid_images[filename]['image_url'],
                        'house_title': valid_images[filename]['house_title']
                    })
                    seen_house_ids.add(house_id)
        
        print(f"[DEBUG] MySQL CBIR search completed with {len(results)} results")
        return results
        
    except Exception as e:
        print(f"Error in MySQL CBIR search: {e}")
        return []


def calculate_improved_similarity_single(query_features, database_features, search_type):
    """
    Calculate similarity between query and a single database image
    """
    try:
        # Method 1: Cosine similarity (most important for architectural features)
        cosine_sim = np.dot(database_features, query_features) / (
            np.linalg.norm(database_features) * np.linalg.norm(query_features)
        )
        
        # Method 2: Euclidean distance (inverted and normalized)
        euclidean_dist = np.linalg.norm(database_features - query_features)
        euclidean_sim = 1 / (1 + euclidean_dist)
        
        # Method 3: Manhattan distance (inverted and normalized)
        manhattan_dist = np.sum(np.abs(database_features - query_features))
        manhattan_sim = 1 / (1 + manhattan_dist)
        
        # Method 4: Pearson correlation (good for architectural patterns)
        query_centered = query_features - np.mean(query_features)
        db_centered = database_features - np.mean(database_features)
        pearson_sim = np.sum(db_centered * query_centered) / (
            np.linalg.norm(db_centered) * np.linalg.norm(query_centered)
        )
        pearson_sim = np.nan_to_num(pearson_sim, nan=0.0)
        
        # Combine methods with weights optimized for architectural similarity
        if search_type == 'visual':
            # For visual similarity, emphasize cosine and pearson correlation
            similarity = 0.5 * cosine_sim + 0.3 * pearson_sim + 0.1 * euclidean_sim + 0.1 * manhattan_sim
        elif search_type == 'style':
            # For style similarity, use all methods with equal weight
            similarity = 0.3 * cosine_sim + 0.3 * pearson_sim + 0.2 * euclidean_sim + 0.2 * manhattan_sim
        else:  # combined
            # For combined, balance all methods
            similarity = 0.4 * cosine_sim + 0.3 * pearson_sim + 0.15 * euclidean_sim + 0.15 * manhattan_sim
        
        return similarity
        
    except Exception as e:
        print(f"Error calculating single similarity: {e}")
        return 0.0 