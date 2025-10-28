# EduLink

## Overview
EduLink is a student resource-sharing platform where seniors can share educational materials with juniors. Students can upload and download notes, books, past year questions (PYQs), and useful links.

## Current State
- **Type**: Full-stack web application (Frontend + Backend)
- **Frontend**: Static HTML/CSS/JavaScript with Bootstrap 5
- **Backend**: Python Flask REST API
- **Storage**: Browser localStorage (client-side only)
- **Servers**: 
  - Frontend: Python HTTP server on port 5000
  - Backend: Flask API server on port 8000 (localhost)

## Project Structure
### Frontend
- `index.html` - Landing page with welcome message and feature overview
- `login2.html` - Login page with localStorage authentication
- `signup.html` - Signup page for new users
- `page1.html` - Main dashboard where users upload/download resources
- `*.svg` - Icon files for UI elements
- `*.jpeg` - Image assets for the website

### Backend
- `app.py` - Flask application with REST API endpoints
- `requirements.txt` - Python dependencies (Flask, Flask-CORS)

## Features
1. **User Authentication**: Sign up and login using localStorage
2. **Resource Sharing**: Upload files or links categorized as:
   - Books
   - Notes
   - PYQs (Past Year Questions)
   - Links
3. **Resource Discovery**: Search and filter resources by category
4. **User Profile**: View personal uploads and downloads history
5. **Duplicate Prevention**: Checks for duplicate files and similar descriptions

## Technical Details
### Frontend
- Vanilla JavaScript with Bootstrap 5 for responsive UI
- All data stored in browser localStorage
- File sharing uses blob URLs (createObjectURL)
- SHA-256 hashing for duplicate file detection

### Backend
- Flask 3.1.2 REST API
- Flask-CORS enabled for cross-origin requests
- API endpoint: `/api/data` returns JSON status message

## Recent Changes
- **October 19, 2025**: Added Flask backend with REST API
  - Created `app.py` with `/api/data` endpoint
  - Generated `requirements.txt` with Flask dependencies
  - Updated workflow to run both frontend and backend servers
  - Backend runs on localhost:8000, frontend on port 5000
- **Initial Setup**: 
  - Fixed JavaScript template literal syntax errors in page1.html
  - Converted Windows line endings to Unix format
  - Set up Python HTTP server for development
  - Created replit.md documentation

## Running the Project
The project runs two servers simultaneously:
1. **Frontend**: Python HTTP server on port 5000 (serves static HTML/CSS/JS files)
2. **Backend**: Flask API server on localhost:8000 (provides REST API endpoints)

Both servers start automatically with the workflow. Access the frontend at the Replit webview URL.

## API Endpoints
- `GET /api/data` - Returns a simple status message
  ```json
  {
    "status": "ok",
    "data": "Hello from the backend!"
  }
  ```

## Environment Variables
- `FLASK_DEBUG` - Set to `true` to enable Flask debug mode (default: `false`). Debug mode should only be enabled for local development and troubleshooting.

## Known Limitations
- Data is only stored locally in browser (not persistent across browsers/devices)
- File uploads create blob URLs that are session-specific
- No real authentication or user management system
- No database backend
