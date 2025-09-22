#!/usr/bin/env python3
"""
Database-based CBIR search functionality
"""

import os
import numpy as np
import pickle
from cbir_search import extract_feature, extract_style_feature, should_exclude_image

# Import database connection from main app
try:
    from app import app, mysql
except ImportError:
    # Fallback: create minimal Flask app for standalone use
    from flask import Flask
    from flask_mysqldb import MySQL
    import os
    
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = os.environ.get('MYSQLHOST', 'localhost')
    app.config['MYSQL_USER'] = os.environ.get('MYSQLUSER', 'root')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQLPASSWORD', '')
    app.config['MYSQL_DB'] = os.environ.get('MYSQLDATABASE', 'projectdb')
    app.config['MYSQL_PORT'] = int(os.environ.get('MYSQLPORT', '3307'))
    app.config['MYSQL_UNIX_SOCKET'] = os.environ.get('MYSQL_UNIX_SOCKET')
    app.config['MYSQL_CONNECT_TIMEOUT'] = 10
    app.config['MYSQL_USE_UNICODE'] = True
    app.config['MYSQL_CHARSET'] = 'utf8mb4'
    app.config['MYSQL_COLLATION'] = 'utf8mb4_general_ci'
    
    mysql = MySQL(app)

def search_similar_images_db(query_image_path, top_k=6, search_type='visual', filters=None):
    """
    Search for similar images using database-stored embeddings
    
    Args:
        query_image_path: Path to the query image
        top_k: Number of similar images to return
        search_type: Type of search ('visual', 'style', 'combined')
        filters: Dictionary of filters (price_min, price_max, bedrooms, house_type, etc.)
    
    Returns:
        List of dictionaries with filename, similarity score, and house metadata
    """
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            
            # Extract features for the query image
            if search_type == 'visual':
                query_feat = extract_feature(query_image_path)
                embedding_type = 'visual'
            elif search_type == 'style':
                query_feat = extract_style_feature(query_image_path)
                embedding_type = 'style'
            elif search_type == 'combined':
                query_feat = extract_feature(query_image_path)
                embedding_type = 'visual'
            else:
                raise ValueError(f"Unknown search type: {search_type}")

            # Build the base query with house metadata - ONLY use main images
            base_query = """
                SELECT ie.image_id, ie.house_id, ie.image_url, ie.embedding,
                       h.h_title, h.price, h.bedrooms, h.bathrooms, h.living_area,
                       t.t_name as house_type, p.p_name as project_name
                FROM image_embeddings ie
                JOIN house h ON ie.house_id = h.h_id
                JOIN house_images hi ON ie.image_id = hi.id AND hi.is_main = 1
                LEFT JOIN house_type t ON h.t_id = t.t_id
                LEFT JOIN project p ON h.p_id = p.p_id
                WHERE ie.embedding_type = %s
            """
            
            query_params = [embedding_type]
            
            # Add filters if provided
            if filters:
                if filters.get('price_min'):
                    base_query += " AND h.price >= %s"
                    query_params.append(filters['price_min'])
                
                if filters.get('price_max'):
                    base_query += " AND h.price <= %s"
                    query_params.append(filters['price_max'])
                
                if filters.get('bedrooms'):
                    base_query += " AND h.bedrooms = %s"
                    query_params.append(filters['bedrooms'])
                
                if filters.get('house_type'):
                    base_query += " AND h.t_id = %s"
                    query_params.append(filters['house_type'])
                
                if filters.get('project'):
                    base_query += " AND h.p_id = %s"
                    query_params.append(filters['project'])

            # Execute query
            cur.execute(base_query, query_params)
            db_results = cur.fetchall()
            cur.close()

            print(f"[DEBUG] Found {len(db_results)} main images with embeddings for comparison")
            
            if not db_results:
                print("No main images with embeddings found in database")
                return []

            # Get query image filename to exclude it from results
            query_filename = os.path.basename(query_image_path)
            print(f"[DEBUG] Excluding query image: {query_filename}")
            
            # Process results and compute similarities
            results = []
            for row in db_results:
                image_id, house_id, image_url, embedding_blob, title, price, bedrooms, bathrooms, area, house_type, project_name = row
                
                # Extract filename for filtering
                filename = image_url.split('/')[-1] if '/' in image_url else image_url
                
                # Skip the query image itself
                if filename == query_filename:
                    print(f"[DEBUG] Skipping query image: {filename}")
                    continue
                
                # Filter out non-photographic images
                if should_exclude_image(filename):
                    continue
                
                # Deserialize embedding
                try:
                    db_embedding = pickle.loads(embedding_blob)
                except:
                    print(f"Error deserializing embedding for image {image_id}")
                    continue
                
                # Compute cosine similarity
                similarity = np.dot(db_embedding, query_feat) / (
                    np.linalg.norm(db_embedding) * np.linalg.norm(query_feat) + 1e-10
                )
                
                # Debug: Log similarity calculation
                print(f"[DEBUG] Similarity for {filename}: {similarity:.4f}")
                
                results.append({
                    'image_id': image_id,
                    'house_id': house_id,
                    'filename': filename,
                    'image_url': image_url,
                    'similarity': float(similarity),
                    'title': title,
                    'price': price,
                    'bedrooms': bedrooms,
                    'bathrooms': bathrooms,
                    'area': area,
                    'house_type': house_type,
                    'project_name': project_name
                })

            # Sort by similarity (descending) and return top-k
            results.sort(key=lambda x: x['similarity'], reverse=True)
            
            return results[:top_k]

    except Exception as e:
        print(f"Error in database CBIR search: {e}")
        import traceback
        traceback.print_exc()
        return []

def add_embedding_to_db(image_id, house_id, image_url, embedding, embedding_type='visual'):
    """
    Add a new embedding to the database
    
    Args:
        image_id: ID of the image in house_images table
        house_id: ID of the house
        image_url: URL of the image
        embedding: Numpy array of the embedding
        embedding_type: Type of embedding ('visual' or 'style')
    """
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            
            # Serialize embedding
            embedding_blob = pickle.dumps(embedding)
            
            # Insert into database
            cur.execute("""
                INSERT INTO image_embeddings 
                (image_id, house_id, image_url, embedding, embedding_type)
                VALUES (%s, %s, %s, %s, %s)
            """, (image_id, house_id, image_url, embedding_blob, embedding_type))
            
            mysql.connection.commit()
            cur.close()
            
            print(f"✅ Added {embedding_type} embedding for image {image_id}")
            return True
            
    except Exception as e:
        print(f"❌ Error adding embedding: {e}")
        return False

def update_house_embeddings(house_id):
    """
    Update embeddings for all images of a specific house
    
    Args:
        house_id: ID of the house to update
    """
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            
            # Get all images for this house
            cur.execute("""
                SELECT id, image_url FROM house_images 
                WHERE house_id = %s AND image_url IS NOT NULL
            """, (house_id,))
            
            images = cur.fetchall()
            cur.close()
            
            updated_count = 0
            
            for img_id, image_url in images:
                # Construct full path
                image_path = f"static/uploads/{image_url.split('/')[-1]}"
                
                # Check if image exists
                import os
                if not os.path.exists(image_path):
                    print(f"⚠️  Image not found: {image_path}")
                    continue
                
                # Extract features
                try:
                    visual_embedding = extract_feature(image_path)
                    style_embedding = extract_style_feature(image_path)
                    
                    # Add visual embedding
                    if add_embedding_to_db(img_id, house_id, image_url, visual_embedding, 'visual'):
                        updated_count += 1
                    
                    # Add style embedding
                    if add_embedding_to_db(img_id, house_id, image_url, style_embedding, 'style'):
                        updated_count += 1
                        
                except Exception as e:
                    print(f"❌ Error processing {image_path}: {e}")
                    continue
            
            print(f"✅ Updated {updated_count} embeddings for house {house_id}")
            return True
            
    except Exception as e:
        print(f"❌ Error updating house embeddings: {e}")
        return False

if __name__ == "__main__":
    # Test the database-based search
    test_image = 'static/uploads/100051498_163247088548284_6174265717089632256_n.jpg_1755597611.png'
    
    print("Testing database-based CBIR search...")
    results = search_similar_images_db(test_image, top_k=3, search_type='visual')
    
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results):
        print(f"  {i+1}. {result['filename']} - {result['similarity']:.4f}")
        print(f"      House: {result['title']} - {result['price']:,} THB")
        print(f"      Type: {result['house_type']} - {result['bedrooms']} bedrooms")
        print()
