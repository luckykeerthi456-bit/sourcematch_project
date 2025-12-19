# SourceMatch - Explainable AI for Recruitment

A full-stack recruitment platform that uses AI to match job seekers with job opportunities. The system provides transparency through explainable AI, showing recruiters why candidates match specific roles.

## Features

### Core Functionality
- **Candidate Resume Scoring**: Upload resume → AI scoring against job requirements
- **Job Matching**: Intelligent matching between candidate skills and job requirements
- **Recruiter Portal**: Review applications, view candidate profiles, accept/reject candidates
- **User Authentication**: Secure login/registration for candidates and recruiters
- **Explainable Scoring**: View which skills matched and why candidates received specific scores

### Technical Highlights
- **Explainable AI**: Uses sentence-transformers embeddings with skill extraction
- **Responsive UI**: React frontend with modern styling
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Database**: SQLite with SQLAlchemy ORM
- **Resume Parsing**: Automatic text extraction and fingerprinting from PDF/DOC

## Project Structure

```
sourcematch_project/
├── backend/                    # FastAPI backend
│   ├── main.py                # App entry point with CORS & routes
│   ├── auth.py                # JWT token generation & validation
│   ├── models.py              # SQLAlchemy models (User, Job, Application, etc.)
│   ├── schemas.py             # Pydantic request/response schemas
│   ├── routes/
│   │   ├── users.py           # Register, login endpoints
│   │   ├── jobs.py            # Job CRUD endpoints
│   │   └── applications.py    # Application scoring, recruiter portal
│   └── utils/
│       ├── parser.py          # Resume text extraction & fingerprinting
│       └── scoring.py         # AI scoring logic with skill extraction
├── frontend/                   # React frontend
│   ├── public/
│   │   └── index.html         # Entry point
│   ├── src/
│   │   ├── App.jsx            # Main app component with routing
│   │   ├── LoginPage.jsx      # Login/Register UI
│   │   ├── Dashboard.jsx      # Candidate dashboard (job search & apply)
│   │   └── RecruiterDashboard.jsx  # Recruiter portal (manage applications)
│   ├── package.json           # npm dependencies
│   └── index.js               # React entry point
├── ml/
│   └── scoring_service.py     # ML model wrapper (lazy-loads embeddings)
├── requirements-backend.txt   # Python dependencies
├── README.md                  # This file
└── sourcematch.db             # SQLite database (created at first run)
```

## Quick Start

### Backend Setup (Python)

```powershell
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-backend.txt

# Start the backend (runs on http://localhost:8000)
python -m uvicorn backend.main:app --reload --port 8000
```

Expected startup output:
```
[STARTUP] Initializing database...
[STARTUP] Database initialized successfully
[STARTUP] Creating resumes directory...
[STARTUP] All startup tasks completed
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Frontend Setup (Node.js + React)

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000` (check console for exact URL).

## API Endpoints

### Authentication
- `POST /api/users/register` - Register new user (candidate or recruiter)
- `POST /api/users/login` - Login with email & password

### Jobs (Candidate View)
- `GET /api/jobs` - List all available jobs
- `POST /api/score` - Upload resume and get scored job matches (top 10)
- `POST /api/apply` - Apply for a specific job

### Applications & Scoring
- `GET /api/applications/recruiter/applications` - Recruiter: list applications
- `GET /api/applications/recruiter/applications/{id}` - Recruiter: view application details with candidate profile
- `PUT /api/applications/recruiter/applications/{id}/status` - Recruiter: update application status (JSON or form-encoded)

### Match History
- `GET /api/applications/history` - List past resume scoring sessions

## Usage

### As a Candidate
1. Open http://localhost:3000 in your browser
2. Register with email, password, and full name
3. Login to access the candidate dashboard
4. Upload your resume and browse job matches
5. Click "View" to see why you're matched for specific roles
6. Click "Apply" to submit application

### As a Recruiter
1. Register as a recruiter (select "Recruiter" in role dropdown)
2. Login to access recruiter portal
3. View all applications from candidates
4. Click on an application to see:
   - Candidate profile (DOB, course, graduation year, skills)
   - Resume preview
   - AI match score and explanation
   - Matched skills
5. Click **Shortlist** to advance candidate
6. Click **Reject** to decline candidate

## Key Technologies

### Backend
- **FastAPI**: Modern, fast web framework with automatic API docs
- **SQLAlchemy**: ORM for database interactions
- **Pydantic**: Data validation and serialization
- **sentence-transformers**: Pre-trained embeddings for semantic matching
- **python-multipart**: Multipart form data handling
- **PyPDF2**: PDF resume extraction

### Frontend
- **React 18**: UI library with hooks
- **Axios**: HTTP client for API calls

### ML & NLP
- **all-MiniLM-L6-v2**: Sentence transformer model (6M parameters, fast)
- **spaCy**: Optional NLP pipeline for enhanced entity extraction

## Troubleshooting

### Backend won't start: "ModuleNotFoundError: No module named 'fastapi'"
- Ensure virtual environment is activated
- Re-run: `python -m pip install -r requirements-backend.txt`
- Or create a fresh venv: `python -m venv .venv` and reinstall

### Frontend dev server doesn't start or shows network error
- Check npm is installed: `npm --version`
- Delete `node_modules` folder and run: `npm install`
- If port 3000 is in use, the dev server will use the next available port

### Resume upload fails: "File not found" or permission errors
- Ensure `resumes/` directory exists (backend creates it at startup)
- Check write permissions on the project directory
- Try uploading a simpler PDF without special encoding

### Status update (Reject/Shortlist) returns 422 error
- Check browser DevTools Network tab for exact request/response
- Backend now accepts both form-encoded and JSON `{status: "rejected"}`
- Ensure proper Content-Type header is set

## Database Schema

### Users Table
- `id` (PK), `email`, `password_hash`, `full_name`, `role`, `created_at`

### Jobs Table
- `id`, `title`, `description`, `requirements`, `company`, `location`, `salary`, `experience`, `required_skills`, `recruiter_id` (FK), `created_at`

### Applications Table
- `id`, `job_id` (FK), `candidate_id` (FK), `resume_path`, `resume_text`, `fingerprint`, `score` (0.0-1.0 normalized), `explanation` (JSON), `status`, `created_at`

## Recent Improvements

1. **Score Normalization**: All scores properly normalized to 0-100% range
2. **Recruiter UI**: Added missing candidate profile fields (DOB, course, year_of_passing, skills)
3. **Job Model Extension**: Added company, location, salary, experience, required_skills
4. **Login Endpoint**: Updated to accept JSON payload
5. **Status Update Endpoint**: Now accepts both form-encoded and JSON body
6. **ML Lazy Loading**: Sentence-transformer model lazy-loads on first use (no startup blocking)
7. **FormData Header Fix**: Removed manual Content-Type for proper multipart boundary

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and test locally
3. Commit: `git commit -m "Description of changes"`
4. Push: `git push origin feature/your-feature`
5. Open a pull request

## License

MIT License

## Support

For issues or questions:
- Check the troubleshooting section above
- Review API docs at http://localhost:8000/docs (when backend is running)
- Check browser console and network logs for error details

## Release: Merge summary (my/local-changes → main)

- Release tag: merge commit 5b48718d (2025-12-19)
- Branch merged: `my/local-changes` into `main`
- Highlights:
   - Frontend: added a styled `ConfirmModal` and a small `Toast` component for consistent confirmations and brief notifications.
   - Frontend: Recruiter portal improvements — Users tab (list/delete users), application delete flow wired to modal, and better status update logging.
   - Backend: safe resume file cleanup when deleting applications or match searches (only deletes files under `resumes/`).
   - Backend: fixed DB session lifecycle issues (short-lived sessions via `get_db()` / SessionLocal) and avoided DetachedInstanceError by copying needed ORM fields before closing sessions.
   - Tests: added TestClient-based scripts for apply/delete/history flows to prevent regressions.
   - Misc: small UX and auth fixes — axios restores Authorization header from localStorage and auto-logout on 401/403.

If you want this release summarized as a GitHub release or tagged, tell me the tag name (e.g., `v0.2.0`) and I'd create it and push the tag.
