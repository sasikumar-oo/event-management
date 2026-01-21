import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g, flash, render_template_string
from functools import wraps

from models import db, Service, Work, Enquiry, User, Setting

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key_for_dev')

# Absolute path for Render compatibility
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database.db')
# Force absolute path as requested for Render
RENDER_DB_PATH = '/opt/render/project/src/database.db'
if os.path.exists('/opt/render/project/src'):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{RENDER_DB_PATH}'
else:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', SQLALCHEMY_DATABASE_URI)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def init_db():
    with app.app_context():
        db.create_all()
        # Seed admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()

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
    # Use EXACT status match as requested
    services_data = Service.query.filter_by(status='ACTIVE').order_by(Service.order.asc()).limit(3).all()
    works_data = Work.query.filter_by(status='VISIBLE').order_by(Work.id.desc()).limit(3).all()
    
    return render_template('index.html', services=services_data, works=works_data)

@app.route('/about')
@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/services')
@app.route('/services.html')
def services():
    # Fetch all ACTIVE services without limit, using models
    services_data = Service.query.filter_by(status='ACTIVE').order_by(Service.order.asc()).all()
    return render_template('services.html', services=services_data)

@app.route('/works')
@app.route('/events')
@app.route('/events.html')
@app.route('/works.html')
def works():
    # Fetch all VISIBLE works without limit, using models
    works_data = Work.query.filter_by(status='VISIBLE').order_by(Work.id.desc()).all()
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
        services = Service.query.all()
        works = Work.query.all()
        enquiries = Enquiry.query.all()
        # Mock bookings as they aren't fully implemented in models.py yet but used in dashboard
        bookings = [] 
        
        return render_template('admin/dashboard.html', 
                               services_count=len(services), 
                               works_count=len(works), 
                               enquiries_count=len(enquiries),
                               bookings_count=len(bookings),
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
    services = Service.query.all()
    return render_template_string(SERVICES_TEMPLATE, services=services)

@app.route('/admin/services/add', methods=['GET', 'POST'])
@login_required
def admin_services_add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status'] # User said must be ACTIVE (uppercase)
        icon = request.form.get('icon', 'fa-check')
        
        new_service = Service(
            title=title,
            short_desc=description,
            full_desc=description,
            icon=icon,
            status=status
        )
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for('admin_services_list'))
    return render_template_string(ADD_SERVICE_TEMPLATE)

@app.route('/admin/services/delete/<int:id>', methods=['POST'])
@login_required
def admin_services_delete(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for('admin_services_list'))

# --- API Routes for Dashboard SPA ---
@app.route('/api/services', methods=['GET'])
def api_get_services():
    services = Service.query.all()
    return {"services": [
        {
            "id": s.id,
            "title": s.title,
            "shortDesc": s.short_desc,
            "fullDesc": s.full_desc,
            "icon": s.icon,
            "image": s.image,
            "active": s.status == 'ACTIVE',
            "order": s.order,
            "status": s.status
        } for s in services
    ]}

@app.route('/api/services', methods=['POST'])
@login_required
def api_save_service():
    data = request.json
    service_id = data.get('id')
    
    if service_id and str(service_id).startswith('svc_'):
        # This is a temp ID from the SPA, treat as new
        service = None
    elif service_id:
        service = Service.query.get(service_id)
    else:
        service = None
        
    if not service:
        service = Service()
        db.session.add(service)
        
    service.title = data.get('title')
    service.short_desc = data.get('shortDesc')
    service.full_desc = data.get('fullDesc')
    service.icon = data.get('icon')
    service.image = data.get('image')
    service.order = data.get('order', 0)
    service.status = 'ACTIVE' if data.get('active') else 'INACTIVE'
    
    db.session.commit()
    return {"status": "success", "id": service.id}

@app.route('/api/services/<int:id>', methods=['DELETE'])
@login_required
def api_delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return {"status": "success"}

@app.route('/api/works', methods=['GET'])
def api_get_works():
    works = Work.query.all()
    return {"works": [
        {
            "id": w.id,
            "title": w.title,
            "category": w.category,
            "location": w.location,
            "date": w.date,
            "description": w.description,
            "image": w.image,
            "active": w.status == 'VISIBLE',
            "status": w.status
        } for w in works
    ]}

@app.route('/api/works', methods=['POST'])
@login_required
def api_save_work():
    data = request.json
    work_id = data.get('id')
    
    if work_id and str(work_id).startswith('work_'):
        work = None
    elif work_id:
        work = Work.query.get(work_id)
    else:
        work = None
        
    if not work:
        work = Work()
        db.session.add(work)
        
    work.title = data.get('title')
    work.category = data.get('category')
    work.location = data.get('location')
    work.date = data.get('date')
    work.description = data.get('description')
    work.image = data.get('image')
    work.status = 'VISIBLE' if data.get('active') else 'HIDDEN'
    
    db.session.commit()
    return {"status": "success", "id": work.id}

@app.route('/api/works/<int:id>', methods=['DELETE'])
@login_required
def api_delete_work(id):
    work = Work.query.get_or_404(id)
    db.session.delete(work)
    db.session.commit()
    return {"status": "success"}

# Ensure DB exists
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
