from app import app, mysql

def check_house_structure():
    with app.app_context():
        cur = mysql.connection.cursor()
        
        # Check house table structure
        cur.execute("DESCRIBE house")
        print("\nHouse table structure:")
        for col in cur.fetchall():
            print(f"- {col[0]} ({col[1]})")
            
        # Check house_features table
        cur.execute("SELECT * FROM house_features")
        print("\nHouse features:")
        for row in cur.fetchall():
            print(f"- ID: {row[0]}, Name: {row[1]}")
            
        # Check sample house data with features
        cur.execute("""
            SELECT h.h_id, h.h_title, h.f_id, hf.f_name 
            FROM house h
            LEFT JOIN house_features hf ON h.f_id = hf.id
            LIMIT 5
        """)
        print("\nSample houses with features:")
        for row in cur.fetchall():
            print(f"- House: {row[1]} (ID: {row[0]}), Feature: {row[3]} (ID: {row[2]})")
            
        cur.close()

if __name__ == "__main__":
    check_house_structure()
