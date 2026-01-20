import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g, flash, render_template_string
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key_for_dev')
DATABASE = 'database.db'

# --- Database Helper ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        # Services table - Expanded for template compatibility
        # content: id, title, short_desc, full_desc, icon, status
        db.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                short_desc TEXT,
                full_desc TEXT,
                icon TEXT DEFAULT 'fa-check',
                status TEXT NOT NULL,
                "order" INTEGER DEFAULT 0
            )
        ''')
        # Works table
        db.execute('''
            CREATE TABLE IF NOT EXISTS works (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT,
                location TEXT,
                date TEXT,
                description TEXT,
                image TEXT,
                status TEXT NOT NULL
            )
        ''')
        db.commit()

# --- Context Processor (Template Compatibility) ---
@app.context_processor
def inject_settings():
    # Mock settings to prevent template errors
    # In a full app, these would come from a Settings table
    site_settings = {
        'siteName': 'Ap Events',
        'footerText': 'Creating timeless memories with elegance and style.',
        'phone': '+1 (555) 123-4567',
        'email': 'info@apevents.com',
        'address': '123 Luxury Lane, Event City'
    }
    return dict(site_settings=site_settings)

# --- Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Public Routes ---
@app.route('/')
@app.route('/index.html')
def home():
    db = get_db()
    # Fetch ALL active/visible records and slice in Python as requested
    all_services = db.execute('SELECT * FROM services WHERE status = "ACTIVE" ORDER BY "order" ASC').fetchall()
    all_works = db.execute('SELECT * FROM works WHERE status = "VISIBLE" ORDER BY date DESC').fetchall()
    
    services_data = all_services[:3]
    works_data = all_works[:3]
    
    print("DEBUG: Home page - Services count:", len(all_services))
    print("DEBUG: Home page - Works count:", len(all_works))
    
    return render_template('index.html', services=services_data, works=works_data)

@app.route('/about')
@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/services')
@app.route('/services.html')
def services():
    db = get_db()
    # Fetch all ACTIVE services without limit
    services_data = db.execute('SELECT * FROM services WHERE status = "ACTIVE" ORDER BY "order" ASC').fetchall()
    print("Services count:", len(services_data))
    return render_template('services.html', services=services_data)

@app.route('/works')
@app.route('/events')
@app.route('/events.html')
@app.route('/works.html')
def works():
    db = get_db()
    # Fetch all VISIBLE works without limit
    works_data = db.execute('SELECT * FROM works WHERE status = "VISIBLE" ORDER BY date DESC').fetchall()
    print("Works count:", len(works_data))
    return render_template('works.html', works=works_data)

@app.route('/booking')
@app.route('/booking.html')
def booking():
    return render_template('booking.html')

@app.route('/contact', methods=['GET', 'POST'])
@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Enquiry received!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# --- Admin Routes ---
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    try:
        db = get_db()
        # Fetch data and convert to dict for JSON serialization safety in templates
        services_rows = db.execute('SELECT * FROM services').fetchall()
        services = [dict(row) for row in services_rows]
        
        # Defensive fetching for works
        try:
            works_rows = db.execute('SELECT * FROM works').fetchall()
            works = [dict(row) for row in works_rows]
        except Exception as e:
            print("DASHBOARD DEBUG: Works query failed:", e)
            works = []
            
        # Count logic
        services_count = len(services)
        works_count = len(works)
        
        # Enquiries handling
        enquiries_count = 0
        enquiries = []
        try:
            enquiries_rows = db.execute('SELECT * FROM enquiries').fetchall()
            enquiries = [dict(row) for row in enquiries_rows]
            enquiries_count = len(enquiries)
        except Exception as e:
            print("DASHBOARD DEBUG: Enquiries query failed:", e)
            
        # Bookings handling
        bookings_count = 0
        bookings = []
        try:
            bookings_rows = db.execute('SELECT * FROM bookings').fetchall()
            bookings = [dict(row) for row in bookings_rows]
            bookings_count = len(bookings)
        except Exception as e:
            print("DASHBOARD DEBUG: Bookings query failed:", e)

        print(f"DASHBOARD DEBUG: counts - services:{services_count}, works:{works_count}, enquiries:{enquiries_count}, bookings:{bookings_count}")

        return render_template('admin/dashboard.html', 
                               services_count=services_count, 
                               works_count=works_count, 
                               enquiries_count=enquiries_count,
                               bookings_count=bookings_count,
                               services=services, 
                               works=works, 
                               enquiries=enquiries,
                               bookings=bookings)
    except Exception as e:
        print("DASHBOARD ERROR:", e)
        raise


# --- Admin Services CRUD (New Requirements) ---
SERVICES_TEMPLATE = '''
<!doctype html>
<title>Manage Services</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
<div class="container mt-5">
    <h1>Services</h1>
    <a href="{{ url_for('admin_services_add') }}" class="btn btn-primary mb-3">Add New Service</a>
    <a href="{{ url_for('admin_dashboard') }}" class="btn btn-secondary mb-3">Back to Dashboard</a>
    <table class="table">
        <thead>
            <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for service in services %}
            <tr>
                <td>{{ service.title }}</td>
                <td>{{ service.short_desc }}</td>
                <td>{{ service.status }}</td>
                <td>
                    <form action="{{ url_for('admin_services_delete', id=service.id) }}" method="post" onsubmit="return confirm('Are you sure?');">
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
'''

ADD_SERVICE_TEMPLATE = '''
<!doctype html>
<title>Add Service</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
<div class="container mt-5">
    <h1>Add Service</h1>
    <form method="post">
        <div class="mb-3">
            <label class="form-label">Title</label>
            <input type="text" name="title" class="form-control" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Description</label>
            <textarea name="description" class="form-control" required></textarea>
        </div>
        <div class="mb-3">
            <label class="form-label">Icon (FontAwesome class, e.g., fa-star)</label>
            <input type="text" name="icon" class="form-control" value="fa-check">
        </div>
        <div class="mb-3">
            <label class="form-label">Status</label>
            <select name="status" class="form-control">
                <option value="ACTIVE">ACTIVE</option>
                <option value="INACTIVE">INACTIVE</option>
            </select>
        </div>
        <button type="submit" class="btn btn-success">Save</button>
        <a href="{{ url_for('admin_services_list') }}" class="btn btn-secondary">Cancel</a>
    </form>
</div>
'''

@app.route('/admin/services')
@login_required
def admin_services_list():
    db = get_db()
    services = db.execute('SELECT * FROM services').fetchall()
    return render_template_string(SERVICES_TEMPLATE, services=services)

@app.route('/admin/services/add', methods=['GET', 'POST'])
@login_required
def admin_services_add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        icon = request.form.get('icon', 'fa-check')
        
        # Save description to both short and full desc for template compatibility
        db = get_db()
        db.execute('INSERT INTO services (title, short_desc, full_desc, icon, status) VALUES (?, ?, ?, ?, ?)',
                   (title, description, description, icon, status))
        db.commit()
        return redirect(url_for('admin_services_list'))
    return render_template_string(ADD_SERVICE_TEMPLATE)

@app.route('/admin/services/delete/<int:id>', methods=['POST'])
@login_required
def admin_services_delete(id):
    db = get_db()
    db.execute('DELETE FROM services WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('admin_services_list'))

# Ensure DB exists (Deployment compatibility)
if not os.path.exists(DATABASE):
    init_db()

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
