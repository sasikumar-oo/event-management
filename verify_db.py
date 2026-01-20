from app import app, init_db, DATABASE
import sqlite3
import os

def verify():
    print(f"Target Database: {DATABASE}")
    
    # Trigger initialization from app.py
    print("Re-initializing database via app.init_db()...")
    init_db()

    if not os.path.exists(DATABASE):
        print(f"Error: {DATABASE} still does not exist after init_db().")
        return

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("\n--- Verifying Schema ---")
    try:
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        print(f"Tables found: {[t['name'] for t in tables]}")
        
        for table in ['services', 'works']:
            cols = cursor.execute(f"PRAGMA table_info({table})").fetchall()
            print(f"Columns for {table}: {[c['name'] for c in cols]}")
            
    except Exception as e:
        print(f"Schema error: {e}")

    print("\n--- Inserting Mock Data ---")
    try:
        # Clear existing
        cursor.execute("DELETE FROM services")
        cursor.execute("DELETE FROM works")
        
        cursor.execute('''
            INSERT INTO services (title, short_desc, full_desc, icon, status, "order")
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Wedding Planning', 'Elegant weddings.', 'Full weddings services.', 'fa-ring', 'Active', 1))
        
        cursor.execute('''
            INSERT INTO works (title, category, location, date, description, image, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('Summer Gala', 'Corporate', 'Beach Club', '2025-07-20', 'A beautiful summer party.', 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622', 'Visible'))
        
        conn.commit()
        print("Mock data inserted successfully.")
        
    except Exception as e:
        print(f"Insertion error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    verify()
