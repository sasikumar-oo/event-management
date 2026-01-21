import sqlite3
import os
from flask import Flask
from models import db, Service, Work

DATABASE = 'database.db'

def diagnostic():
    print(f"Checking for {DATABASE}...")
    if not os.path.exists(DATABASE):
        print(f"ERROR: {DATABASE} not found at {os.path.abspath(DATABASE)}")
        return

    print(f"--- SQLite3 PRAGMA check ---")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    for table in ['services', 'works']:
        print(f"\nTable: {table}")
        cursor.execute(f"PRAGMA table_info({table})")
        cols = cursor.fetchall()
        for col in cols:
            print(f"  {col}")
    conn.close()

    print(f"\n--- SQLAlchemy Query check ---")
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath(DATABASE)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        try:
            s = Service.query.first()
            print(f"Successfully queried Service. Image field value: {getattr(s, 'image', 'N/A') if s else 'No records'}")
        except Exception as e:
            print(f"Failed to query Service: {e}")

        try:
            w = Work.query.first()
            print(f"Successfully queried Work. Image field value: {getattr(w, 'image', 'N/A') if w else 'No records'}")
        except Exception as e:
            print(f"Failed to query Work: {e}")

if __name__ == '__main__':
    diagnostic()
