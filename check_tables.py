import MySQLdb
from app import mysql

def check_tables():
    try:
        cur = mysql.connection.cursor()
        # Check if house_has_features table exists
        cur.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'projectdb' 
            AND table_name = 'house_has_features'
        """)
        exists = cur.fetchone()[0]
        print(f"house_has_features table exists: {bool(exists)}")
        
        # Check house table structure
        cur.execute("DESCRIBE house")
        print("\nHouse table structure:")
        for col in cur.fetchall():
            print(f"- {col[0]} ({col[1]})")
            
        # Check if any features exist
        cur.execute("SELECT * FROM house_features")
        features = cur.fetchall()
        print(f"\nAvailable features: {[f[1] for f in features]}")
        
        # Check if any houses have features assigned
        if exists:
            cur.execute("""
                SELECT h.h_title, hf.f_name 
                FROM house h
                JOIN house_has_features hhf ON h.h_id = hhf.house_id
                JOIN house_features hf ON hhf.feature_id = hf.id
            """)
            print("\nHouses with features:")
            for row in cur.fetchall():
                print(f"- {row[0]}: {row[1]}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        cur.close()

if __name__ == "__main__":
    check_tables()
