import sqlite3

conn = sqlite3.connect('instance/projectdb.sqlite')
cursor = conn.cursor()

# Show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Available tables:')
for table in tables:
    print(f'  {table[0]}')

# Check house table
cursor.execute('SELECT h_id, h_title, status FROM house LIMIT 5')
houses = cursor.fetchall()
print('\nHouses:')
for house in houses:
    print(f'  ID: {house[0]}, Title: {house[1]}, Status: {house[2]}')

# Check if there are any image-related columns in house table
cursor.execute("PRAGMA table_info(house)")
columns = cursor.fetchall()
print('\nHouse table columns:')
for col in columns:
    print(f'  {col[1]} - {col[2]}')

conn.close()
