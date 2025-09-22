import sqlite3

conn = sqlite3.connect('instance/projectdb.sqlite')
cursor = conn.cursor()

# Check embeddings count
cursor.execute('SELECT COUNT(*) FROM image_embeddings')
count = cursor.fetchone()[0]
print(f'Total embeddings in database: {count}')

# Check house images count
cursor.execute('SELECT COUNT(*) FROM house_images')
img_count = cursor.fetchone()[0]
print(f'Total house images in database: {img_count}')

# Check active houses
cursor.execute('SELECT COUNT(*) FROM house WHERE status = "active"')
house_count = cursor.fetchone()[0]
print(f'Active houses: {house_count}')

# Show sample embeddings
if count > 0:
    cursor.execute('SELECT house_id, image_url FROM image_embeddings LIMIT 5')
    samples = cursor.fetchall()
    print('\nSample embeddings:')
    for house_id, image_url in samples:
        print(f'  House {house_id}: {image_url}')

conn.close()
