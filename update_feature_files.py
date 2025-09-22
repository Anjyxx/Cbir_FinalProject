import sqlite3
import numpy as np
import os

def update_feature_files():
    """Update the feature files to match the current database embeddings"""
    
    # Connect to database
    conn = sqlite3.connect('instance/projectdb.sqlite')
    cursor = conn.cursor()
    
    # Get all embeddings from database
    cursor.execute("""
        SELECT ie.image_url, ie.embedding 
        FROM image_embeddings ie 
        ORDER BY ie.image_id
    """)
    results = cursor.fetchall()
    
    print(f"Found {len(results)} embeddings in database")
    
    if not results:
        print("No embeddings found in database!")
        conn.close()
        return
    
    # Extract features and filenames
    features = []
    filenames = []
    
    for image_url, embedding_blob in results:
        # Convert blob back to numpy array
        embedding = np.frombuffer(embedding_blob, dtype=np.float32)
        features.append(embedding)
        
        # Extract filename from URL
        if image_url.startswith('uploads/'):
            filename = image_url[8:]  # Remove 'uploads/' prefix
        else:
            filename = image_url
        filenames.append(filename)
    
    # Convert to numpy arrays
    features_array = np.array(features)
    filenames_array = np.array(filenames)
    
    print(f"Created arrays: {features_array.shape[0]} features, {len(filenames_array)} filenames")
    
    # Create backup of existing files
    features_file = 'static/features/house_features.npy'
    filenames_file = 'static/features/filenames.npy'
    
    if os.path.exists(features_file):
        os.rename(features_file, features_file + '.bak')
        print(f"Backed up {features_file}")
    
    if os.path.exists(filenames_file):
        os.rename(filenames_file, filenames_file + '.bak')
        print(f"Backed up {filenames_file}")
    
    # Save new feature files
    np.save(features_file, features_array)
    np.save(filenames_file, filenames_array)
    
    print(f"Saved {features_file} with shape {features_array.shape}")
    print(f"Saved {filenames_file} with {len(filenames_array)} filenames")
    
    # Verify the files
    loaded_features = np.load(features_file)
    loaded_filenames = np.load(filenames_file)
    
    print(f"Verification: {loaded_features.shape[0]} features, {len(loaded_filenames)} filenames")
    
    conn.close()
    print("Feature files updated successfully!")

if __name__ == "__main__":
    update_feature_files()
