# 🚀 Quick Start - SourceMatch with Secure Login

## What You Now Have

✅ **Secure Database Authentication** - Users stored in SQLite with hashed passwords
✅ **React Login/Register UI** - Beautiful gradient interface with form validation
✅ **JWT Token System** - Secure stateless authentication
✅ **Session Persistence** - Auto-login on page refresh
✅ **Complete Backend** - FastAPI with all endpoints ready

---

## 30-Second Start

### Option A: Automated
```powershell
cd c:\Users\2025\Desktop\sourcematch_project
start.bat
```
This opens Backend and Frontend in separate windows automatically.

### Option B: Manual (2 terminals)
**Terminal 1:**
```powershell
cd c:\Users\2025\Desktop\sourcematch_project
python backend/main.py
```

**Terminal 2:**
```powershell
cd c:\Users\2025\Desktop\sourcematch_project\frontend
npm start
```

---

## Access Points

| Component | URL | Purpose |
|-----------|-----|---------|
| Frontend | http://localhost:3000 | React app - Login/Dashboard |
| Backend API | http://localhost:8000 | FastAPI endpoints |
| API Docs | http://localhost:8000/docs | Swagger documentation |
| API Docs (ReDoc) | http://localhost:8000/redoc | Alternative API docs |

---

## Test Credentials (After Registration)

Create a test account:
- **Email**: test@example.com
- **Password**: test1234
- **Role**: Candidate

---

## Key Features

### Login Page
- Email + Password login
- Registration with name + role selection
- Form validation (password match, min length)
- Error messages for invalid credentials
- "Remember me" via localStorage

### Dashboard (After Login)
- Display logged-in user info
- Show email and role
- Logout button
- Ready to add: Job feed, Resume scorer, Search history

---

## React Components

| File | Purpose |
|------|---------|
| `App.jsx` | Main component - manages auth state and routing |
| `LoginPage.jsx` | Beautiful login/register UI |
| `Dashboard.jsx` | User dashboard after login |
| `index.js` | React app entry point |
| `index.css` | Global styles |

---

## Backend Endpoints

### Authentication
```
POST /api/users/register     → Create new account
POST /api/users/login        → Login and get JWT token
```

### Resume Scoring (Already Built)
```
POST /api/applications/score     → Upload resume & score against jobs
GET  /api/applications/history   → View past searches
```

### Jobs (Already Built)
```
GET  /api/jobs               → List all jobs
POST /api/jobs               → Create job (admin)
```

---

## Database

- **Type**: SQLite
- **File**: `sourcematch.db` (auto-created)
- **User Table**: Stores email, hashed_password, name, role
- **Auto-Reset**: Delete `sourcematch.db` file to reset database

---

## Common Tasks

### Register New User
1. Open http://localhost:3000
2. Click "Register" tab
3. Fill form and submit
4. Auto-logged in to Dashboard

### Login
1. On LoginPage, click "Login" tab
2. Enter email and password
3. Click "Login"
4. See Dashboard

### Logout
1. Click "Logout" button
2. Back to LoginPage
3. Session cleared from localStorage

### Reset Everything
```powershell
# Delete database
Remove-Item c:\Users\2025\Desktop\sourcematch_project\sourcematch.db

# Restart backend (will auto-create new DB)
python backend/main.py
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | Kill the process: `netstat -ano \| findstr :8000` then `taskkill /pid <PID>` |
| Port 3000 already in use | Run on different port: `PORT=3001 npm start` |
| "Cannot find module" | Run `npm install` in frontend directory |
| Database locked | Delete `sourcematch.db` and restart backend |
| CORS errors | Ensure backend is http://localhost:8000, frontend is http://localhost:3000 |

---

## File Locations

```
sourcematch_project/
├── frontend/src/
│   ├── App.jsx              ← Main authentication logic
│   ├── LoginPage.jsx        ← Login/Register UI
│   ├── Dashboard.jsx        ← Authenticated dashboard
│   ├── index.js
│   └── index.css
├── backend/
│   ├── main.py              ← FastAPI app
│   ├── auth.py              ← Password hashing & JWT
│   ├── models.py            ← Database models
│   └── routes/
│       └── users.py         ← Login/Register endpoints
├── sourcematch.db           ← SQLite database (auto-created)
└── start.bat                ← Quick start script
```

---

## What's Working

✅ User registration with password hashing
✅ User login with JWT token generation
✅ Token storage in localStorage
✅ Session persistence on page refresh
✅ Logout functionality
✅ Form validation and error messages
✅ Beautiful responsive UI
✅ Secure password requirements
✅ Database persistence

---

## Next Steps

1. **Test it out** - Start the app and create some accounts
2. **Integrate features** - Add job feed, resume scorer to Dashboard
3. **Deploy** - Use Heroku, AWS, or any hosting platform
4. **Customize** - Change colors, add more fields, add social login

---

## Support

For more details, see:
- `LOGIN_IMPLEMENTATION_COMPLETE.md` - Full technical documentation
- `AUTHENTICATION_SETUP.md` - Setup and running instructions
- `README.md` - Project overview

---

**You're all set! Run `start.bat` and test the login system.** 🎉
