from app import app, mysql

def check_house_data():
    with app.app_context():
        cur = mysql.connection.cursor()
        
        # Check houses with feature ID 8 (2 ห้องนอน)
        cur.execute("""
            SELECT h.h_id, h.h_title, h.f_id, hf.f_name 
            FROM house h
            LEFT JOIN house_features hf ON h.f_id = hf.f_id
            WHERE h.f_id = 8
        """)
        
        print("\nHouses with feature ID 8 (2 ห้องนอน):")
        houses = cur.fetchall()
        if houses:
            for house in houses:
                print(f"- House: {house['h_title']} (ID: {house['h_id']})")
        else:
            print("No houses found with feature ID 8")
            
        # Count total houses
        cur.execute("SELECT COUNT(*) as total FROM house")
        total = cur.fetchone()[0]
        print(f"\nTotal houses in database: {total}")
        
        # Count houses with any feature
        cur.execute("SELECT COUNT(*) as with_feature FROM house WHERE f_id IS NOT NULL")
        with_feature = cur.fetchone()[0]
        print(f"Houses with any feature assigned: {with_feature}")
        
        # Check if any houses have features assigned at all
        cur.execute("SELECT h_id, h_title, f_id FROM house WHERE f_id IS NOT NULL")
        houses_with_features = cur.fetchall()
        print("\nHouses with features assigned:")
        for house in houses_with_features:
            print(f"- House: {house[1]} (ID: {house[0]}), Feature ID: {house[2]}")
        
        # Show feature distribution
        print("\nFeature distribution:")
        cur.execute("""
            SELECT hf.f_id, hf.f_name, COUNT(h.h_id) as house_count
            FROM house_features hf
            LEFT JOIN house h ON hf.f_id = h.f_id
            GROUP BY hf.f_id, hf.f_name
        """)
        for row in cur.fetchall():
            print(f"- {row['f_name']} (ID: {row['f_id']}): {row['house_count']} houses")
            
        cur.close()

if __name__ == "__main__":
    check_house_data()
