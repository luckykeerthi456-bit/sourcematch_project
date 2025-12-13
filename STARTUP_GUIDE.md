# 🚀 SourceMatch - Complete Startup Guide

## Quick Start (Easiest Way)

### Windows PowerShell
```powershell
cd c:\Users\2025\Desktop\sourcematch_project
.\start.ps1
```

This will automatically start both backend and frontend in separate windows.

---

## Manual Start (If You Prefer)

### Terminal 1: Start Backend
```powershell
cd c:\Users\2025\Desktop\sourcematch_project
.\venv\Scripts\Activate.ps1
python run_backend.py
```

Expected output:
```
============================================================
Starting SourceMatch Backend
============================================================
Project Root: C:\Users\2025\Desktop\sourcematch_project
API will be available at http://localhost:8000
API Docs at http://localhost:8000/docs
Press Ctrl+C to stop
============================================================

INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Terminal 2: Start Frontend
```powershell
cd c:\Users\2025\Desktop\sourcematch_project\frontend
npm start
```

Expected output:
```
Compiled successfully!

You can now view sourcematch in the browser.

Local:            http://localhost:3000
On Your Network:  http://[your-ip]:3000

Note that the development build is not optimized.
To create a production build, use: npm run build
```

---

## Test the Application

1. **Open Frontend**: Navigate to `http://localhost:3000` in your browser
2. **Register**: 
   - Click "Register" tab
   - Enter: Full Name, Email, Password, Role
   - Click "Register"
3. **Login**:
   - After registration, you should be logged in
   - If logged out, use the email and password to login
4. **Verify**:
   - You should see your name and email on the Dashboard
   - Click "Logout" to test logout functionality

---

## URLs & Endpoints

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | React application |
| Backend API | http://localhost:8000 | FastAPI server |
| Swagger Docs | http://localhost:8000/docs | Interactive API documentation |
| ReDoc Docs | http://localhost:8000/redoc | Alternative API documentation |

---

## API Endpoints (for Testing)

### User Management
```
POST /api/users/register          Register new user
POST /api/users/login             Login user
```

### Resume Scoring
```
POST /api/applications/score      Upload resume and score against jobs
GET  /api/applications/history    View past searches
```

### Job Management
```
GET  /api/jobs                    List all jobs
```

---

## Troubleshooting

### Port Already in Use
**Problem**: "Address already in use :8000"

**Solution**: 
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with the number)
taskkill /PID 1234 /F

# Or use a different port
$env:BACKEND_PORT=8001
python run_backend.py
```

### Module Not Found
**Problem**: "ModuleNotFoundError: No module named 'fastapi'"

**Solution**:
```powershell
# Activate venv and reinstall dependencies
.\venv\Scripts\Activate.ps1
pip install -r requirements-backend.txt
```

### npm Not Found
**Problem**: "'npm' is not recognized"

**Solution**: 
- Install Node.js from https://nodejs.org/
- Restart terminal after installation
- Run `npm install` in frontend directory

### Database Locked
**Problem**: "database is locked" error

**Solution**:
```powershell
# Delete the database file to reset it
Remove-Item sourcematch.db

# Restart backend (it will create a new database)
python run_backend.py
```

### Frontend Won't Connect to Backend
**Problem**: "Cannot connect to localhost:8000" in browser console

**Solution**:
1. Verify backend is running: http://localhost:8000/docs should work
2. Check CORS is enabled (it is by default)
3. Clear browser cache: Ctrl+Shift+Delete

---

## First Time Setup

If you're starting fresh:

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate venv
python -m venv venv

# 3. Install Python dependencies
pip install -r requirements-backend.txt

# 4. Install Node dependencies (frontend)
cd frontend
npm install
cd ..

# 5. Now ready to start!
.\start.ps1
```

---

## Development Workflow

### Making Backend Changes
1. Edit files in `backend/` directory
2. Backend automatically reloads on file changes (uvicorn watch mode)
3. Test with Swagger docs at http://localhost:8000/docs

### Making Frontend Changes
1. Edit files in `frontend/src/` directory
2. Frontend automatically reloads on file changes (React dev server)
3. Changes appear instantly in browser

### Adding New Python Dependencies
```powershell
.\venv\Scripts\Activate.ps1
pip install package-name
pip freeze > requirements-backend.txt
```

### Adding New Node Dependencies
```powershell
cd frontend
npm install package-name
cd ..
```

---

## Stopping Services

### Method 1: Close Terminal Windows
- Close the backend window (PowerShell with backend running)
- Close the frontend window (PowerShell with React dev server)

### Method 2: Keyboard Shortcuts
- In backend terminal: `Ctrl+C`
- In frontend terminal: `Ctrl+C` (then 'y' to confirm exit)

### Method 3: Kill Process
```powershell
# Stop backend
taskkill /F /IM python.exe  # (stops all Python processes)

# Stop frontend
taskkill /F /IM node.exe    # (stops all Node processes)
```

---

## Checking Service Status

### Is Backend Running?
```powershell
curl http://localhost:8000/docs
# Should return HTML if running
```

### Is Frontend Running?
```powershell
curl http://localhost:3000
# Should return HTML if running
```

---

## Configuration

### Backend Settings
Edit `backend/main.py` to change:
- Host: Change `"0.0.0.0"` to `"127.0.0.1"` for local only
- Port: Change `8000` to another port number
- CORS origins: Edit the middleware configuration

### Frontend Settings
Edit `frontend/src/LoginPage.jsx` or `App.jsx`:
- API URL: Change `http://localhost:8000/api` to your backend URL
- Port: Use `PORT=3001 npm start` for different port

---

## Production Deployment Notes

For production:
1. Build frontend: `cd frontend && npm run build`
2. Serve built files with backend or separate web server
3. Use environment variables for API URLs
4. Use PostgreSQL instead of SQLite
5. Enable HTTPS/SSL
6. Use proper secrets management for JWT key
7. Set CORS properly (don't use "*")

---

## Support & Resources

- **Backend Docs**: http://localhost:8000/docs (when running)
- **Frontend Code**: `frontend/src/App.jsx`, `LoginPage.jsx`, `Dashboard.jsx`
- **Backend Code**: `backend/main.py`, `backend/routes/`
- **Configuration**: `requirements-backend.txt`, `frontend/package.json`

---

**Everything is set up and ready to go! Run `.\start.ps1` to begin.** 🎉
