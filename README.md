# EduLink

## Running the Application

### Prerequisites
- Python 3.x
- Flask and its dependencies (install using requirements.txt)
- A modern web browser
- VS Code with Live Server extension (recommended)

### Setup Instructions

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the Flask backend:
```bash
# For Windows PowerShell:
$env:FLASK_DEBUG="true"
python app.py

# For Command Prompt:
set FLASK_DEBUG=true
python app.py
```

The backend will start on http://127.0.0.1:8000

3. Serve the frontend:
- Using VS Code: Right-click on `index.html` and select "Open with Live Server"
- The frontend should open in your browser at http://127.0.0.1:5500 or a similar port

## Database (SQLite or MySQL)

- Default: SQLite file at `edulink.db` in the project root (auto-created on first run).
- Optional: MySQL via `DATABASE_URL` environment variable.

Examples for `DATABASE_URL`:
```bash
# SQLite explicit (same as default)
$env:DATABASE_URL="sqlite:///C:/Users/Chaitanya/OneDrive/Documents/project/edulink-1/edulink-1/edulink.db"

# MySQL (requires a running MySQL server and a database named edulink)
$env:DATABASE_URL="mysql+pymysql://username:password@localhost:3306/edulink"
```

Tables are auto-created on startup. A test user (`test_user`, `test@example.com`) is seeded if missing.

## API Endpoints

- `GET /api/health` – Server status
- `GET /api/users` – List users
- `POST /api/users` – Create user `{ username, email }`
- `GET /api/courses` – List courses with instructor names
- `POST /api/courses` – Create course `{ title, description?, instructor_id }`
- `POST /upload` – Upload a file (multipart form, field name: `file`)
- `GET /files` – List uploaded files
- `GET /download/<filename>` – Download specific file

## Frontend Integration

The current `js/api.js` uses Firebase (Firestore/Storage). If you want the frontend to talk to the Flask backend instead, you can:
- Call the REST endpoints above from your own JS (fetch/axios), or
- Replace `js/api.js` with a version that points to `http://127.0.0.1:8000` and implements the same functions against the Flask API.

Firebase scripts are included in `index.html`, and a placeholder config is in `js/firebase-init.js`.

## Switching to Firebase (Frontend)

This project can use Firebase instead of the Flask backend for data and file storage. The repository includes a Firebase initialization placeholder at `js/firebase-init.js` and a Firebase-backed API at `js/api.js`.

Steps to enable Firebase:

1. Create a Firebase project at https://console.firebase.google.com/
2. In the project, enable Firestore (Native mode) and Storage.
3. Obtain your Firebase config object (Project Settings > General > Your apps > SDK setup and configuration).
4. Open `js/firebase-init.js` and replace the placeholder values in `firebaseConfig` with your project's values.
5. Open `index.html` with Live Server (or serve it from any static host). The Firebase CDN scripts are already included in `index.html`.
6. The frontend exposes Firebase operations via `window.api` (see `js/api.js`).

Important: Keep your credentials safe. For production, restrict Firestore/Storage rules and consider using environment variables or server-side proxy for sensitive operations.

## Troubleshooting

1. CORS Issues:
   - Ensure the backend is running on port 8000
   - Check that your frontend URL is allowed in the CORS configuration
   - Verify network requests in browser developer tools

2. File Upload Issues:
   - Check file size (max 16MB)
   - Ensure the uploads directory exists
   - Verify file permissions

3. Connection Issues:
   - Confirm both frontend and backend are running
   - Check console for error messages
   - If using MySQL, verify `DATABASE_URL`, network connectivity, and that `pymysql` is installed (`pip install pymysql`)