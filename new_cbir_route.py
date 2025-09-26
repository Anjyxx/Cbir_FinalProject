#!/usr/bin/env python3
"""
New CBIR Routes with Improved System
Uses the old working CBIR system that connects to real database
"""

from flask import request, render_template, session, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from house_validator import validate_house_image

def add_new_cbir_routes(app, mysql, dict_fetchall, dict_fetchone, csrf):
    """Add new CBIR routes to the Flask app"""
    
    @csrf.exempt
    @app.route('/search_by_image_new', methods=['GET', 'POST'])
    def search_by_image_new():
        """New improved CBIR search route"""
        if request.method == 'GET':
            # Handle GET requests for filtering on image search results
            print(f"[DEBUG] GET request to search_by_image_new")
            query_image = request.args.get('query_image') or session.get('cbir_query_image_new')
            print(f"[DEBUG] Query image: {query_image}")
            
            if not query_image:
                # If no query image, show empty results with message
                cur = mysql.connection.cursor()
                
                # Get dropdown data for the filter bar
                cur.execute("SELECT t_id as id, t_name as name FROM house_type WHERE status = 'active' ORDER BY t_name")
                house_types = dict_fetchall(cur)
                
                cur.execute("SELECT p_id as id, p_name as name FROM project WHERE status = 'active' ORDER BY p_name")
                projects = dict_fetchall(cur)
                
                cur.execute("SELECT f_id as id, f_name as name FROM house_features WHERE status = 'active' ORDER BY f_name")
                features = dict_fetchall(cur)
                
                cur.close()
                
                return render_template('results.html', 
                                     houses=[], 
                                     house_types=house_types,
                                     projects=projects,
                                     features=features,
                                     message="กรุณาทำการค้นหาด้วยรูปภาพก่อน",
                                     current_route='search_by_image_new')
            
            # Get all houses and CBIR results from session
            all_houses = session.get('all_houses_new', [])
            cbir_house_ids = set(session.get('cbir_house_ids_new', []))
            
            if not all_houses:
                # Fetch all houses from database
                cur = mysql.connection.cursor()
                cur.execute("""
                    SELECT h.h_id as id, h.h_title as title, h.h_description as description, 
                           h.price, h.bedrooms, h.bathrooms, h.living_area as area,
                           h.t_id, h.p_id, h.status,
                           t.t_name as type_name, p.p_name as project_name
                    FROM house h
                    LEFT JOIN house_type t ON h.t_id = t.t_id
                    LEFT JOIN project p ON h.p_id = p.p_id
                    WHERE h.status NOT IN ('inactive', 'sold')
                    ORDER BY h.h_id
                """)
                all_houses = dict_fetchall(cur)
                cur.close()
            
            # Mark CBIR houses and get similarity scores from session
            cbir_house_ids_set = set(cbir_house_ids)
            similarity_scores = session.get('cbir_similarity_scores_new', {})
            
            for house in all_houses:
                house['is_cbir_result'] = house['id'] in cbir_house_ids_set
                house_id_str = str(house['id'])
                house_id_int = house['id']
                similarity = similarity_scores.get(house_id_str) or similarity_scores.get(house_id_int, 0.0)
                house['similarity'] = similarity
                house['gallery_images'] = []
            
            # Get filter parameters
            selected_project = request.args.get('project', '')
            selected_type = request.args.get('house_type', '')
            selected_bedrooms = request.args.get('bedrooms', '')
            selected_feature = request.args.get('feature', '')
            min_price = request.args.get('min_price', '')
            max_price = request.args.get('max_price', '')
            min_area = request.args.get('min_area', '')
            max_area = request.args.get('max_area', '')
            sort = request.args.get('sort', 'similarity')
            
            # Start with only CBIR results
            if cbir_house_ids:
                filtered_houses = [house for house in all_houses if house.get('id') in cbir_house_ids]
                for house in filtered_houses:
                    house['is_cbir_result'] = True
            else:
                filtered_houses = [house for house in all_houses if house.get('is_cbir_result', False)]
            
            # Apply filters
            if selected_project:
                filtered_houses = [h for h in filtered_houses if str(h.get('p_id')) == selected_project]
            if selected_type:
                filtered_houses = [h for h in filtered_houses if str(h.get('t_id')) == selected_type]
            if selected_bedrooms:
                filtered_houses = [h for h in filtered_houses if str(h.get('bedrooms')) == selected_bedrooms]
            if min_price:
                filtered_houses = [h for h in filtered_houses if h.get('price', 0) >= float(min_price)]
            if max_price:
                filtered_houses = [h for h in filtered_houses if h.get('price', 0) <= float(max_price)]
            if min_area:
                filtered_houses = [h for h in filtered_houses if h.get('area', 0) >= float(min_area)]
            if max_area:
                filtered_houses = [h for h in filtered_houses if h.get('area', 0) <= float(max_area)]
            
            # Sort results
            if sort == 'price_low':
                filtered_houses.sort(key=lambda x: x.get('price', 0))
            elif sort == 'price_high':
                filtered_houses.sort(key=lambda x: x.get('price', 0), reverse=True)
            elif sort == 'area_low':
                filtered_houses.sort(key=lambda x: x.get('area', 0))
            elif sort == 'area_high':
                filtered_houses.sort(key=lambda x: x.get('area', 0), reverse=True)
            else:  # similarity
                filtered_houses.sort(key=lambda x: x.get('similarity', 0), reverse=True)
            
            # Get dropdown data
            cur = mysql.connection.cursor()
            cur.execute("SELECT t_id as id, t_name as name FROM house_type WHERE status = 'active' ORDER BY t_name")
            house_types = dict_fetchall(cur)
            
            cur.execute("SELECT p_id as id, p_name as name FROM project WHERE status = 'active' ORDER BY p_name")
            projects = dict_fetchall(cur)
            
            cur.execute("SELECT f_id as id, f_name as name FROM house_features WHERE status = 'active' ORDER BY f_name")
            features = dict_fetchall(cur)
            cur.close()
            
            return render_template('results.html', 
                                 houses=filtered_houses,
                                 house_types=house_types,
                                 projects=projects,
                                 features=features,
                                 query_image=query_image,
                                 current_route='search_by_image_new')
        
        # Handle POST requests (image upload)
        file = request.files.get('query_img') or request.files.get('file')
        if not file:
            return "No file part in request.", 400
        
        if file.filename == '':
            return "No selected file.", 400
        
        # Validate file
        if file and file.filename:
            filename = secure_filename(file.filename)
            timestamp = str(int(datetime.now().timestamp()))
            unique_filename = f"{timestamp}_{filename}"
            
            # Create uploads directory if it doesn't exist
            upload_dir = 'static/uploads/queries'
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save file
            upload_path = os.path.join(upload_dir, unique_filename)
            file.save(upload_path)
            
            # Validate that it's a house image
            try:
                is_valid, validation_message, validation_info = validate_house_image(upload_path)
                if not is_valid:
                    # Clean up the uploaded file
                    if os.path.exists(upload_path):
                        os.remove(upload_path)
                    
                    # Get dropdown data for error page
                    cur = mysql.connection.cursor()
                    cur.execute("SELECT t_id as id, t_name as name FROM house_type WHERE status = 'active' ORDER BY t_name")
                    house_types = dict_fetchall(cur)
                    
                    cur.execute("SELECT p_id as id, p_name as name FROM project WHERE status = 'active' ORDER BY p_name")
                    projects = dict_fetchall(cur)
                    
                    cur.execute("SELECT f_id as id, f_name as name FROM house_features WHERE status = 'active' ORDER BY f_name")
                    features = dict_fetchall(cur)
                    cur.close()
                    
                    return render_template('results.html', 
                                         houses=[], 
                                         house_types=house_types,
                                         projects=projects,
                                         features=features,
                                         message=validation_message,
                                         validation_error=True,
                                         current_route='search_by_image_new')
                
                print(f"[VALIDATION] Image validated as house: {validation_message}")
                
            except Exception as e:
                print(f"[ERROR] House validation failed: {e}")
                # Continue anyway but log the error
        
        # Run CBIR search using the old working system
        search_type = request.form.get('search_type', 'visual')
        
        # Get filters from form
        filters = {}
        if request.form.get('min_price'):
            filters['min_price'] = float(request.form.get('min_price'))
        if request.form.get('max_price'):
            filters['max_price'] = float(request.form.get('max_price'))
        if request.form.get('min_area'):
            filters['min_area'] = float(request.form.get('min_area'))
        if request.form.get('max_area'):
            filters['max_area'] = float(request.form.get('max_area'))
        if request.form.get('bedrooms'):
            filters['bedrooms'] = int(request.form.get('bedrooms'))
        if request.form.get('house_type'):
            filters['house_type'] = int(request.form.get('house_type'))
        if request.form.get('project'):
            filters['project'] = int(request.form.get('project'))
        
        # Use the old working CBIR system that connects to real database
        try:
            print(f"[DEBUG] Starting CBIR search with search_type={search_type}")
            from cbir_search import search_similar_images
            
            # Load valid images from database first
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT hi.image_url, hi.house_id, h.h_title
                FROM house_images hi
                JOIN house h ON hi.house_id = h.h_id
                WHERE h.status = 'available'
            """)
            valid_images = {}
            for row in cur.fetchall():
                image_url, house_id, house_title = row
                img_filename = os.path.basename(image_url)
                valid_images[img_filename] = {
                    'house_id': house_id,
                    'house_title': house_title,
                    'image_url': image_url
                }
            cur.close()
            
            print(f"[DEBUG] Loaded {len(valid_images)} valid images from database")
            if len(valid_images) == 0:
                print("[ERROR] No valid images found in database!")
                # Fallback: try without status filter
                cur = mysql.connection.cursor()
                cur.execute("""
                    SELECT hi.image_url, hi.house_id, h.h_title
                    FROM house_images hi
                    JOIN house h ON hi.house_id = h.h_id
                """)
                for row in cur.fetchall():
                    image_url, house_id, house_title = row
                    img_filename = os.path.basename(image_url)
                    valid_images[img_filename] = {
                        'house_id': house_id,
                        'house_title': house_title,
                        'image_url': image_url
                    }
                cur.close()
                print(f"[DEBUG] Fallback: Loaded {len(valid_images)} images without status filter")
            
            # Run improved CBIR search with valid images
            from cbir_search import search_similar_images_mysql
            results = search_similar_images_mysql(upload_path, top_k=50, search_type=search_type, valid_images=valid_images)
            print(f"[DEBUG] CBIR search completed with {len(results)} results:")
            for i, result in enumerate(results):
                print(f"[DEBUG]   {i+1}. {result.get('filename', 'N/A')} - similarity: {result.get('similarity', 0):.4f}")
            
            # Filter results to show similarity between 70%-95% (higher quality threshold)
            filtered_results = []
            for result in results:
                similarity = result.get('similarity', 0)
                if 0.70 <= similarity <= 0.95:
                    filtered_results.append(result)
                    print(f"[DEBUG] Keeping result with similarity: {similarity:.4f}")
                else:
                    print(f"[DEBUG] Filtering out result with similarity: {similarity:.4f}")
            
            results = filtered_results
            print(f"[DEBUG] After filtering (70%-95% similarity): {len(results)} results")
            
        except Exception as e:
            print(f"[ERROR] CBIR search failed: {e}")
            import traceback
            traceback.print_exc()
            results = []
        
        # Process results using the old working approach
        if not results:
            print("[DEBUG] No CBIR results, showing fallback houses")
            # Show some houses from database as fallback
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT h.h_id as id, h.h_title as title, h.h_description as description, 
                       h.price, h.bedrooms, h.bathrooms, h.living_area as area,
                       h.t_id, h.p_id, h.status,
                       t.t_name as type_name, p.p_name as project_name
                FROM house h
                LEFT JOIN house_type t ON h.t_id = t.t_id
                LEFT JOIN project p ON h.p_id = p.p_id
                WHERE h.status NOT IN ('inactive', 'sold')
                ORDER BY h.h_id
                LIMIT 4
            """)
            houses = dict_fetchall(cur)
            
            # Add default similarity scores
            for house in houses:
                house['similarity'] = 0.5  # Default similarity
                house['is_cbir_result'] = False
                house['gallery_images'] = []
                house['main_image_url'] = '/static/img/house_placeholder.jpg'
            
            cur.close()
            
            # Get dropdown data
            cur = mysql.connection.cursor()
            cur.execute("SELECT t_id as id, t_name as name FROM house_type WHERE status = 'active' ORDER BY t_name")
            house_types = dict_fetchall(cur)
            
            cur.execute("SELECT p_id as id, p_name as name FROM project WHERE status = 'active' ORDER BY p_name")
            projects = dict_fetchall(cur)
            
            cur.execute("SELECT f_id as id, f_name as name FROM house_features WHERE status = 'active' ORDER BY f_name")
            features = dict_fetchall(cur)
            cur.close()
            
            return render_template('results.html',
                                 houses=houses,
                                 house_types=house_types,
                                 projects=projects,
                                 features=features,
                                 query_image=f'/static/uploads/queries/{unique_filename}',
                                 message="ไม่พบบ้านที่คล้ายกัน แสดงบ้านตัวอย่าง",
                                 current_route='search_by_image_new')
        
        # Process CBIR results using the old working approach
        print(f"[DEBUG] Processing {len(results)} CBIR results...")
        
        # Group results by house_id and get the best match for each house
        house_best_matches = {}
        for result in results:
            print(f"[DEBUG] Processing result: {result}")
            if 'house_id' in result and result['house_id'] is not None:
                house_id = result['house_id']
                if house_id not in house_best_matches or result['similarity'] > house_best_matches[house_id]['similarity']:
                    house_best_matches[house_id] = {
                        'filename': result['filename'],
                        'similarity': result['similarity'],
                        'image_url': result.get('image_url', ''),
                        'house_title': result.get('house_title', '')
                    }
                    print(f"[DEBUG] Added house {house_id} with similarity {result['similarity']:.4f}")
            else:
                print(f"[DEBUG] Result missing house_id: {result}")
        
        print(f"[DEBUG] Found {len(house_best_matches)} house matches")
        
        if not house_best_matches:
            print("[DEBUG] No house matches found, showing fallback houses")
            # Fallback: show some houses from database
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT h.h_id as id, h.h_title as title, h.h_description as description, 
                       h.price, h.bedrooms, h.bathrooms, h.living_area as area,
                       h.t_id, h.p_id, h.status,
                       t.t_name as type_name, p.p_name as project_name
                FROM house h
                LEFT JOIN house_type t ON h.t_id = t.t_id
                LEFT JOIN project p ON h.p_id = p.p_id
                WHERE h.status NOT IN ('inactive', 'sold')
                ORDER BY h.h_id
                LIMIT 4
            """)
            houses = dict_fetchall(cur)
            
            # Add default similarity scores
            for house in houses:
                house['similarity'] = 0.5  # Default similarity
                house['is_cbir_result'] = False
                house['gallery_images'] = []
                house['main_image_url'] = '/static/img/house_placeholder.jpg'
            
            cur.close()
            
            # Get dropdown data
            cur = mysql.connection.cursor()
            cur.execute("SELECT t_id as id, t_name as name FROM house_type WHERE status = 'active' ORDER BY t_name")
            house_types = dict_fetchall(cur)
            
            cur.execute("SELECT p_id as id, p_name as name FROM project WHERE status = 'active' ORDER BY p_name")
            projects = dict_fetchall(cur)
            
            cur.execute("SELECT f_id as id, f_name as name FROM house_features WHERE status = 'active' ORDER BY f_name")
            features = dict_fetchall(cur)
            cur.close()
            
            return render_template('results.html',
                                 houses=houses,
                                 house_types=house_types,
                                 projects=projects,
                                 features=features,
                                 query_image=f'/static/uploads/queries/{unique_filename}',
                                 message="ไม่พบบ้านที่คล้ายกัน แสดงบ้านตัวอย่าง",
                                 current_route='search_by_image_new')
        
        # Get house details from database
        matched_house_ids = list(house_best_matches.keys())
        cur = mysql.connection.cursor()
        format_strings = ','.join(['%s'] * len(matched_house_ids))
        query = f'''
            SELECT h.h_id as id, h.h_title as title, h.h_description as description, 
                   h.price, h.bedrooms, h.bathrooms, h.living_area as area,
                   h.t_id, h.p_id, h.status,
                   t.t_name as type_name, p.p_name as project_name
            FROM house h
            LEFT JOIN house_type t ON h.t_id = t.t_id
            LEFT JOIN project p ON h.p_id = p.p_id
            WHERE h.h_id IN ({format_strings})
            ORDER BY FIELD(h.h_id, {format_strings})
        '''
        cur.execute(query, matched_house_ids + matched_house_ids)
        houses = dict_fetchall(cur)
        
        # Add similarity scores and images
        for house in houses:
            house_id = house['id']
            if house_id in house_best_matches:
                match = house_best_matches[house_id]
                house['similarity'] = match['similarity']
                house['is_cbir_result'] = True
                # Fix image URL - ensure it starts with /static/ and includes houses/ subdirectory
                image_url = match['image_url']
                if image_url and not image_url.startswith('/static/'):
                    if image_url.startswith('uploads/'):
                        # Replace 'uploads/' with '/static/uploads/houses/'
                        image_url = '/static/uploads/houses/' + image_url[8:]  # Remove 'uploads/' prefix
                    elif not image_url.startswith('/'):
                        image_url = '/static/uploads/houses/' + image_url
                house['main_image_url'] = image_url
                print(f"[DEBUG] House {house_id}: similarity={match['similarity']:.4f}, image={image_url}")
            else:
                house['similarity'] = 0.0
                house['is_cbir_result'] = False
                house['main_image_url'] = '/static/img/house_placeholder.jpg'
            
            house['gallery_images'] = []
        
        # Sort by similarity and take top 4
        houses.sort(key=lambda x: x.get('similarity', 0), reverse=True)
        
        # Ensure we have exactly 4 houses
        if len(houses) < 4:
            print(f"[DEBUG] Only {len(houses)} houses found, adding more from database")
            # Get more houses to fill up to 4
            cur = mysql.connection.cursor()
            existing_ids = [h['id'] for h in houses]
            placeholders = ','.join(['%s'] * len(existing_ids))
            query = f"""
                SELECT h.h_id as id, h.h_title as title, h.h_description as description, 
                       h.price, h.bedrooms, h.bathrooms, h.living_area as area,
                       h.t_id, h.p_id, h.status,
                       t.t_name as type_name, p.p_name as project_name
                FROM house h
                LEFT JOIN house_type t ON h.t_id = t.t_id
                LEFT JOIN project p ON h.p_id = p.p_id
                WHERE h.status NOT IN ('inactive', 'sold')
                AND h.h_id NOT IN ({placeholders})
                ORDER BY h.h_id
                LIMIT %s
            """
            cur.execute(query, existing_ids + [4 - len(houses)])
            additional_houses = dict_fetchall(cur)
            
            # Add default similarity scores to additional houses
            for house in additional_houses:
                house['similarity'] = 0.3  # Lower similarity for additional houses
                house['is_cbir_result'] = False
                house['gallery_images'] = []
                house['main_image_url'] = '/static/img/house_placeholder.jpg'
            
            houses.extend(additional_houses)
            cur.close()
        
        houses = houses[:4]  # Show exactly top 4 houses
        print(f"[DEBUG] Final result: {len(houses)} houses to display")
        
        # Store results in session
        session['cbir_results_new'] = results
        session['cbir_query_image_new'] = f'/static/uploads/queries/{unique_filename}'
        session['all_houses_new'] = houses
        session['cbir_house_ids_new'] = matched_house_ids
        session['cbir_similarity_scores_new'] = {str(h['id']): h['similarity'] for h in houses}
        
        # Get dropdown data
        cur = mysql.connection.cursor()
        cur.execute("SELECT t_id as id, t_name as name FROM house_type WHERE status = 'active' ORDER BY t_name")
        house_types = dict_fetchall(cur)
        
        cur.execute("SELECT p_id as id, p_name as name FROM project WHERE status = 'active' ORDER BY p_name")
        projects = dict_fetchall(cur)
        
        cur.execute("SELECT f_id as id, f_name as name FROM house_features WHERE status = 'active' ORDER BY f_name")
        features = dict_fetchall(cur)
        cur.close()
        
        # Fix query image URL - ensure proper path
        query_image_url = f'/static/uploads/queries/{unique_filename}'
        print(f"[DEBUG] Query image URL: {query_image_url}")
        
        # Store query image in session for debugging
        session['query_image'] = query_image_url
        
        return render_template('results.html',
                             houses=houses,
                             house_types=house_types,
                             projects=projects,
                             features=features,
                             query_image=query_image_url,
                             current_route='search_by_image_new')
    
    print("✅ New CBIR routes added successfully")