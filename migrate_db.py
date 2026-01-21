from app import app, db
from models import Service, Work
import sqlite3
import os

DATABASE = 'database.db'

def migrate():
    with app.app_context():
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        print("Starting migration...")

        # 1. Backup old data
        try:
            cursor.execute("ALTER TABLE services RENAME TO services_old")
            cursor.execute("ALTER TABLE works RENAME TO works_old")
        except sqlite3.OperationalError as e:
            print(f"Warning: {e} (Tables might already be renamed or schema partially applied)")

        # 2. Create new tables
        db.create_all()

        # 3. Migrate services
        try:
            cursor.execute("""
                INSERT INTO services (id, title, short_desc, icon, status, "order")
                SELECT id, title, short_desc, icon, status, "order" FROM services_old
            """)
            print("Migrated services data.")
        except Exception as e:
            print(f"Error migrating services: {e}")

        # 4. Migrate works (Mapping 'date' to 'created_at')
        try:
            cursor.execute("""
                INSERT INTO works (id, title, category, location, image, status, created_at)
                SELECT id, title, category, location, image, status, date FROM works_old
            """)
            print("Migrated works data.")
        except Exception as e:
            print(f"Error migrating works: {e}")

        # 5. Drop old tables
        try:
            cursor.execute("DROP TABLE services_old")
            cursor.execute("DROP TABLE works_old")
            print("Dropped old tables.")
        except Exception as e:
            print(f"Error dropping old tables: {e}")

        conn.commit()
        conn.close()
        print("Migration complete.")

if __name__ == '__main__':
    migrate()
