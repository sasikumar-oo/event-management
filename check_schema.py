import sqlite3
import os

db_path = 'database.db'
if not os.path.exists(db_path):
    print(f"File {db_path} not found")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    with open('full_schema.txt', 'w') as f:
        for table in ['services', 'works']:
            f.write(f"--- {table} ---\n")
            cursor.execute(f"PRAGMA table_info({table})")
            for col in cursor.fetchall():
                f.write(f"{col}\n")
    conn.close()
    with open('full_schema.txt', 'r') as f:
        print(f.read())
