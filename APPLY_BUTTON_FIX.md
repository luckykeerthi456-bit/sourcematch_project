# Apply Button Fix - Job Finder Crash Resolution

## Problem
When clicking the **Apply** button in the Job Finder section, the application would close/crash with no clear error message.

## Root Cause
**Payload mismatch between frontend and backend:**

### Frontend was sending (incorrect):
```javascript
{
  job_id: jobId,
  resume_text: resumeFile ? "uploaded" : ""
}
```
- Sent as JSON (`Content-Type: application/json`)
- Missing `candidate_id` field
- Missing actual file upload

### Backend expected (Form fields):
```python
@router.post("/apply", response_model=ApplyResult)
async def apply(
  job_id: int = Form(...),
  candidate_id: int = Form(...),      # ← MISSING
  resume: UploadFile = File(...)      # ← MISSING (expects file, not string)
)
```
- Expected `multipart/form-data` format
- Required: `job_id`, `candidate_id`, `resume` (file)

This mismatch caused the backend to reject the request (422/400 error), which crashed the frontend.

## Solution Applied

### File Modified: `frontend/src/Dashboard.jsx`

Changed the `handleApply` function to:
1. ✅ Use `FormData` for multipart/form-data format
2. ✅ Include `job_id` and `candidate_id` 
3. ✅ Send actual file or create placeholder file if none uploaded
4. ✅ Add console error logging for debugging

```javascript
const handleApply = async (jobId) => {
  try {
    // Prepare FormData with job_id, candidate_id, and resume file
    const formData = new FormData();
    formData.append("job_id", jobId);
    formData.append("candidate_id", user.id);
    
    // If user has uploaded a resume, use it; otherwise create placeholder
    if (resumeFile) {
      formData.append("resume", resumeFile);
    } else {
      const emptyResume = new Blob(["No resume uploaded"], { type: "text/plain" });
      const emptyFile = new File([emptyResume], "resume.txt", { type: "text/plain" });
      formData.append("resume", emptyFile);
    }
    
    await axios.post(API + "/applications/apply", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    setMessage("Applied successfully!");
  } catch (err) {
    console.error("Apply error:", err);
    setMessage(err?.response?.data?.detail || "Failed to apply");
  }
};
```

## Testing Results
✅ **Test Flow:**
1. Register new user → ✅ Success
2. Login with credentials → ✅ Success  
3. Fetch job list → ✅ 8 jobs loaded
4. Apply to job with multipart form → ✅ Status 200 OK

**Backend Response:**
```
INFO: 127.0.0.1:50355 - "POST /api/applications/apply HTTP/1.1" 200 OK
```

## Backend Changes Made

### File: `backend/main.py`
- Added centralized `@app.on_event("startup")` to initialize database and resumes directory
- Moved initialization from router-level handlers to app-level for proper lifecycle management
- Added verbose logging for startup diagnostics

### File: `backend/routes/applications.py`
- Removed duplicate `@router.on_event("startup")` handler (kept in main.py instead)

## Key Differences: Before vs After

| Aspect | Before | After |
|--------|--------|-------|
| **Content-Type** | `application/json` | `multipart/form-data` |
| **Fields** | `job_id`, `resume_text` | `job_id`, `candidate_id`, `resume` |
| **Resume** | String or empty | File object (or placeholder file) |
| **Result** | App crash (422 error) | ✅ Success (200 OK) |

## How to Test Manually

1. **Start services:**
```powershell
cd c:\Users\2025\Desktop\sourcematch_project
$env:BACKEND_PORT=8001
.\venv\Scripts\Activate.ps1

# Terminal 1: Backend
python run_backend.py

# Terminal 2: Frontend
cd frontend
npm start
```

2. **In browser (http://localhost:3000):**
   - Register new account
   - Login
   - Go to "💼 Job Finder" tab
   - Click "Apply" button on any job
   - ✅ Should see "Applied successfully!" message
   - No app crash!

3. **Verify in database:**
```powershell
python view_database.py
# Should show applications count > 0
```

## Related Fixes in Session

- ✅ **Resume Scorer Fix**: Fixed score display by wrapping response in `{ matches: [...] }`
- ✅ **Registration Fix**: Fixed startup event handlers causing server crash
- ✅ **Apply Button Fix**: Fixed payload format mismatch

---

**Status**: ✅ FIXED - Job Apply button now works without crashing!
