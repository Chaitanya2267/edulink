from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from config import Settings
from database import db, init_db, seed_test_data
from database.models import User, Course, Material

app = Flask(__name__, static_folder='.')

# CORS for local file-server usage (e.g., Live Server on port 5500)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5500", "http://127.0.0.1:5500"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

# App configuration
app.config["SQLALCHEMY_DATABASE_URI"] = Settings.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = Settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['UPLOAD_FOLDER'] = Settings.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Settings.MAX_CONTENT_LENGTH

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'Server is running'
    })

# ---- Demo Auth (hardcoded) ----
DEMO_EMAIL = os.getenv('DEMO_EMAIL', 'demo@edulink.local')
DEMO_USERNAME = os.getenv('DEMO_USERNAME', 'demo')
DEMO_PASSWORD = os.getenv('DEMO_PASSWORD', 'demo123')

@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')
    if email == DEMO_EMAIL and password == DEMO_PASSWORD:
        # Ensure demo user exists in DB for downstream relations
        user = User.query.filter_by(email=DEMO_EMAIL).first()
        if not user:
            user = User(username=DEMO_USERNAME, email=DEMO_EMAIL)
            db.session.add(user)
            db.session.commit()
        return jsonify({
            'ok': True,
            'user': { 'id': user.id, 'username': user.username, 'email': user.email }
        })
    return jsonify({'ok': False, 'error': 'Invalid credentials'}), 401

# User endpoints
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.order_by(User.id.asc()).all()
    return jsonify({
        'users': [{
            'id': u.id,
            'username': u.username,
            'email': u.email
        } for u in users]
    })

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json or {}
    try:
        user = User(username=data['username'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 201
    except KeyError:
        db.session.rollback()
        return jsonify({'error': 'Missing required fields'}), 400
    except Exception as e:
        db.session.rollback()
        # Unique constraint errors surface here for both SQLite and MySQL
        return jsonify({'error': str(e)}), 400

# Course endpoints
@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = Course.query.order_by(Course.id.asc()).all()
    return jsonify({
        'courses': [{
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'instructor': (c.instructor.username if c.instructor else None)
        } for c in courses]
    })

@app.route('/api/courses', methods=['POST'])
def create_course():
    data = request.json or {}
    try:
        instructor = User.query.get(int(data['instructor_id']))
        if not instructor:
            return jsonify({'error': 'Invalid instructor_id'}), 400
        course = Course(title=data['title'], description=data.get('description', ''), instructor=instructor)
        db.session.add(course)
        db.session.commit()
        return jsonify({'id': course.id, 'title': course.title, 'description': course.description}), 201
    except KeyError:
        db.session.rollback()
        return jsonify({'error': 'Missing required fields'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# ---- File Upload ----
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    return jsonify({'status': 'File uploaded successfully', 'filename': filename})

# ---- List Uploaded Files ----
@app.route('/files', methods=['GET'])
def list_files():
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---- Download File ----
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    init_db(app)
    seed_test_data(app)
    print('Database initialized successfully!')
    app.run(host='127.0.0.1', port=8000, debug=debug_mode)
