#!/usr/bin/env python3

from app import app, mysql

def check_embeddings():
    with app.app_context():
        cur = mysql.connection.cursor()
        
        # Check total embeddings
        cur.execute('SELECT COUNT(*) FROM image_embeddings')
        total_count = cur.fetchone()[0]
        print(f'Total embeddings in database: {total_count}')
        
        # Check visual embeddings
        cur.execute('SELECT COUNT(*) FROM image_embeddings WHERE embedding_type = "visual"')
        visual_count = cur.fetchone()[0]
        print(f'Visual embeddings: {visual_count}')
        
        # Check style embeddings
        cur.execute('SELECT COUNT(*) FROM image_embeddings WHERE embedding_type = "style"')
        style_count = cur.fetchone()[0]
        print(f'Style embeddings: {style_count}')
        
        # Check if there are any embeddings at all
        if total_count == 0:
            print("❌ No embeddings found in database!")
            print("This explains why the database search is failing and falling back to file-based search.")
        else:
            print("✅ Embeddings found in database")
            
        cur.close()

if __name__ == "__main__":
    check_embeddings()
