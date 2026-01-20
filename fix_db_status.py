import sqlite3
import os

DATABASE = 'database.db'

def fix_status():
    if not os.path.exists(DATABASE):
        print(f"Error: {DATABASE} not found.")
        return

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    print("Updating Services status...")
    cursor.execute("UPDATE services SET status = UPPER(status)")
    print(f"Rows affected: {cursor.rowcount}")

    # Check if works table exists
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='works'").fetchone()
    if tables:
        print("Updating Works status...")
        cursor.execute("UPDATE works SET status = UPPER(status)")
        print(f"Rows affected: {cursor.rowcount}")
    else:
        print("Works table not found.")

    conn.commit()
    conn.close()
    print("Database update complete.")

if __name__ == "__main__":
    fix_status()
