import sqlite3
import os

DATABASE = 'database.db'

def inspect():
    if not os.path.exists(DATABASE):
        print(f"{DATABASE} not found.")
        return

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    with open('schema_output.txt', 'w') as f:
        for table in ['services', 'works']:
            f.write(f"\nSchema for {table}:\n")
            try:
                cursor.execute(f"PRAGMA table_info({table})")
                cols = cursor.fetchall()
                for col in cols:
                    f.write(f"  {col}\n")
            except Exception as e:
                f.write(f"Error inspecting {table}: {e}\n")
    
    conn.close()

if __name__ == '__main__':
    inspect()
