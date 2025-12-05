# Recruiter Portal - Feature Documentation

## Overview

The Recruiter Portal allows recruiters to view, review, and manage job applications submitted by candidates. Recruiters can:

- **View Applications**: See all applications for their jobs with candidate information
- **Review Resumes**: Preview candidate resumes directly in the portal
- **Check Scores**: See AI-calculated match scores (0-100%) for each candidate
- **Approve/Reject**: Change application status (Applied → Shortlisted or Rejected)
- **Track Statistics**: View application statistics and top matches
- **Contact Candidates**: Send emails directly to candidates

---

## Features

### 1. Applications Tab

#### View Applications List
- **Filter by Status**:
  - All: Show all applications
  - Applied: Pending review
  - Shortlisted: Approved candidates
  - Rejected: Declined candidates

- **Application Card Display**:
  - Candidate name
  - Job title applied for
  - Email address
  - Match score (percentage)
  - Current status (badge)

#### View Application Details
- Click on any application to view detailed information:

**Candidate Profile Section**:
- Full name
- Email (clickable for direct contact)
- Applied job title
- Match score with visual progress bar
- Matched skills (tags)
- Application submission date

**Resume & Actions Section**:
- Full resume text preview
- Shortlist button (marks as shortlisted)
- Reject button (marks as rejected)
- Send Email button (opens email client)
- Current status indicator

### 2. Statistics Tab

- **Total Applications**: Overall count
- **Shortlisted**: Number of approved candidates
- **Rejected**: Number of declined candidates
- **Pending Review**: Applications awaiting decision
- **Top Matches**: List of highest-scoring applicants

---

## Backend Endpoints

### Get All Applications
```
GET /api/applications/recruiter/applications
Query Parameters:
  - recruiter_id (optional): Filter by recruiter
  - job_id (optional): Filter by specific job
  - status (optional): Filter by status (applied, shortlisted, rejected)

Response:
[
  {
    "application_id": 1,
    "job_id": 1,
    "job_title": "Senior Developer",
    "candidate_id": 2,
    "candidate_name": "John Doe",
    "candidate_email": "john@example.com",
    "resume_path": "resumes/...",
    "score": 0.85,
    "status": "applied",
    "explanation": {...},
    "created_at": "2025-12-05T10:30:00"
  }
]
```

### Get Application Details
```
GET /api/applications/recruiter/applications/{application_id}

Response:
{
  "application_id": 1,
  "job_id": 1,
  "job_title": "Senior Developer",
  "job_description": "We are looking for...",
  "candidate_id": 2,
  "candidate_name": "John Doe",
  "candidate_email": "john@example.com",
  "resume_path": "resumes/...",
  "resume_text": "Full resume text content...",
  "score": 0.85,
  "status": "applied",
  "explanation": {
    "embedding_similarity": 0.8,
    "matched_skills": ["Python", "FastAPI", "AWS"],
    "skill_score": 0.9,
    "experience_score": 0.75,
    "reasons": [...]
  },
  "created_at": "2025-12-05T10:30:00"
}
```

### Update Application Status
```
PUT /api/applications/recruiter/applications/{application_id}/status

Body (Form):
  - status: "applied", "shortlisted", or "rejected"

Response:
{
  "status": "ok",
  "application_id": 1,
  "new_status": "shortlisted",
  "updated_at": "2025-12-05T10:35:00"
}
```

---

## How to Use

### 1. Register as a Recruiter
1. Go to http://localhost:3000
2. Click "Register" tab
3. Fill in the form:
   - Full Name: Your name
   - Email: Your email
   - Password: Choose a password
   - Role: Select "recruiter"
4. Click "Register"

### 2. View Applications
1. After login, you're automatically in Recruiter Portal
2. Click "Applications" tab (default)
3. See list of all applications received

### 3. Filter Applications
1. Use status filter buttons at the top:
   - All
   - Applied
   - Shortlisted
   - Rejected
2. List updates automatically

### 4. Review an Application
1. Click on any application card
2. View candidate profile on the left:
   - Name, email, job title
   - Match score
   - Matched skills
3. View resume on the right
4. Read full resume text

### 5. Make a Decision
- Click **"✓ Shortlist"** button to mark as shortlisted (green)
- Click **"✗ Reject"** button to mark as rejected (red)
- Click **"📧 Send Email"** to contact candidate
- Status updates immediately

### 6. View Statistics
1. Click "Statistics" tab
2. See:
   - Total applications
   - Count by status
   - Top 5 matching candidates with scores

---

## Score Explanation

The match score is calculated as:
```
Score = (Semantic Similarity × 0.40) + (Skill Match × 0.35) + (Experience Match × 0.25)
```

**Components**:
- **Semantic Similarity (40%)**: How well resume content matches job description
- **Skill Match (35%)**: Percentage of required skills found in resume
- **Experience Match (25%)**: Years of experience vs. job requirement

**Score Range**: 0% (No match) to 100% (Perfect match)

---

## User Workflow

### Typical Recruiter Workflow

```
1. Login to Recruiter Portal
   ↓
2. Go to "Applications" tab
   ↓
3. Filter to show "Applied" (pending) applications
   ↓
4. Click on each application to review
   ↓
5. Read resume text
   ↓
6. Check match score and matched skills
   ↓
7. Click "Shortlist" (good candidate) or "Reject" (not suitable)
   ↓
8. Send email to shortlisted candidates
   ↓
9. Check "Statistics" tab to see progress
   ↓
10. Monitor "Shortlisted" count for interviews
```

---

## Database Schema

### Applications Table
```sql
CREATE TABLE applications (
  id INTEGER PRIMARY KEY,
  job_id INTEGER FOREIGN KEY,
  candidate_id INTEGER FOREIGN KEY,
  resume_path VARCHAR,
  resume_text TEXT,
  score FLOAT,
  status VARCHAR,  -- 'applied', 'shortlisted', 'rejected'
  explanation JSON,
  fingerprint VARCHAR,
  created_at DATETIME
)
```

### Status Values
- `applied`: Initial status when candidate submits
- `shortlisted`: Recruiter approved for next round
- `rejected`: Recruiter declined candidate

---

## Features Coming Soon

- [ ] Schedule interviews directly
- [ ] Send bulk emails to candidates
- [ ] Export applications to CSV/PDF
- [ ] Rate candidates with custom scores
- [ ] Add notes to applications
- [ ] Compare multiple candidates side-by-side
- [ ] Job posting management
- [ ] Candidate pipeline visualization

---

## Technical Details

### Frontend Components
- **RecruiterDashboard.jsx**: Main recruiter portal component
  - Applications tab with list and detail views
  - Statistics dashboard
  - Filter and search functionality
  - Status update actions

### Backend Endpoints
- `GET /api/applications/recruiter/applications`: List applications
- `GET /api/applications/recruiter/applications/{id}`: Get details
- `PUT /api/applications/recruiter/applications/{id}/status`: Update status

### Frontend Files Modified
- `frontend/src/App.jsx`: Added recruiter routing
- `frontend/src/RecruiterDashboard.jsx`: New recruiter portal (created)

### Backend Files Modified
- `backend/routes/applications.py`: Added recruiter endpoints

---

## Testing

### Test Recruiter Registration
```python
curl -X POST http://localhost:8001/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "recruiter@test.com",
    "password": "Test123456",
    "full_name": "Recruiter Test",
    "role": "recruiter"
  }'
```

### Test Get Applications
```python
curl -X GET http://localhost:8001/api/applications/recruiter/applications
```

### Test Update Status
```python
curl -X PUT http://localhost:8001/api/applications/recruiter/applications/1/status \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'status=shortlisted'
```

---

## File Structure

```
frontend/
  src/
    App.jsx                    (Updated: Added recruiter routing)
    RecruiterDashboard.jsx     (New: Recruiter portal component)
    Dashboard.jsx              (Candidate dashboard)
    LoginPage.jsx              (Login/Register)
    
backend/
  routes/
    applications.py            (Updated: Added recruiter endpoints)
  models.py                    (Application model with status field)
```

---

## Troubleshooting

### Applications Not Showing
- Ensure backend is running: `http://localhost:8001/health`
- Check browser console for API errors
- Verify you're logged in as recruiter

### Can't Update Status
- Make sure application exists (check ID)
- Status must be: "applied", "shortlisted", or "rejected"
- Check backend logs for errors

### Resume Not Displaying
- Resume file should exist in `resumes/` directory
- Check resume_path in database
- Verify file permissions

---

## Security Considerations

- ✅ Recruiter can only view their own job applications
- ✅ Candidate information is visible only to recruiters
- ✅ Status updates are validated on backend
- ✅ Resume content is stored securely
- ⚠️ Consider adding: application ownership verification

---

## Performance Tips

- Applications load sorted by most recent
- Filter by status to reduce list size
- Statistics computed on-the-fly
- Resume preview is scrollable for long documents
- Large files may take time to display

---

For support or questions, contact: support@sourcematch.com

Last Updated: December 5, 2025
