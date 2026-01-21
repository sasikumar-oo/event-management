import sqlite3
import os

DATABASE = 'database.db'

def migrate():
    if not os.path.exists(DATABASE):
        print(f"{DATABASE} not found.")
        return

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Table: services
    # Required: id, title, short_desc, full_desc, icon, image, status, "order"
    print("Checking 'services' table...")
    cursor.execute("PRAGMA table_info(services)")
    cols = [col[1] for col in cursor.fetchall()]
    
    if 'image' not in cols:
        print("Adding 'image' to 'services'...")
        cursor.execute("ALTER TABLE services ADD COLUMN image VARCHAR(255)")
    if 'full_desc' not in cols:
        print("Adding 'full_desc' to 'services'...")
        cursor.execute("ALTER TABLE services ADD COLUMN full_desc TEXT")
    if 'status' not in cols:
        print("Adding 'status' to 'services'...")
        cursor.execute("ALTER TABLE services ADD COLUMN status VARCHAR(20)")
    if 'order' not in cols:
        print("Adding 'order' to 'services'...")
        cursor.execute("ALTER TABLE services ADD COLUMN \"order\" INTEGER DEFAULT 0")

    # Table: works
    # Required: id, title, category, location, date, description, image, status, created_at
    print("Checking 'works' table...")
    cursor.execute("PRAGMA table_info(works)")
    cols = [col[1] for col in cursor.fetchall()]

    if 'image' not in cols:
        print("Adding 'image' to 'works'...")
        cursor.execute("ALTER TABLE works ADD COLUMN image VARCHAR(255)")
    if 'date' not in cols:
        print("Adding 'date' to 'works'...")
        cursor.execute("ALTER TABLE works ADD COLUMN date VARCHAR(20)")
    if 'description' not in cols:
        print("Adding 'description' to 'works'...")
        cursor.execute("ALTER TABLE works ADD COLUMN description TEXT")
    if 'status' not in cols:
        print("Adding 'status' to 'works'...")
        cursor.execute("ALTER TABLE works ADD COLUMN status VARCHAR(20)")
    if 'created_at' not in cols:
        print("Adding 'created_at' to 'works'...")
        cursor.execute("ALTER TABLE works ADD COLUMN created_at VARCHAR(50)")

    conn.commit()
    conn.close()
    print("Migration finished successfully.")

if __name__ == '__main__':
    migrate()
