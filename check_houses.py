import sqlite3
import os

# Check what images exist for each house
conn = sqlite3.connect('instance/projectdb.sqlite')
cursor = conn.cursor()

cursor.execute("""
    SELECT hi.house_id, h.h_title, COUNT(*) as image_count
    FROM house_images hi
    JOIN house h ON hi.house_id = h.h_id
    WHERE h.status = 'active'
    GROUP BY hi.house_id, h.h_title
    ORDER BY hi.house_id
""")
houses = cursor.fetchall()

print('Images per house:')
for house_id, title, count in houses:
    print(f'  House {house_id} ({title}): {count} images')

# Check if images exist on disk for house 2
cursor.execute('SELECT house_id, image_url FROM house_images WHERE house_id = 2 LIMIT 5')
house2_images = cursor.fetchall()
print('\nHouse 2 images:')
for house_id, image_url in house2_images:
    full_path = os.path.join('static', image_url)
    exists = os.path.exists(full_path)
    print(f'  {image_url}: {"EXISTS" if exists else "MISSING"}')

conn.close()


