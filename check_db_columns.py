import sqlite3
conn = sqlite3.connect('sourcematch.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(jobs)")
columns = cursor.fetchall()
print("Database jobs table columns:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")
conn.close()
