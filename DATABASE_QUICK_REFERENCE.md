# 📊 SourceMatch Database Quick Reference

## Database Type & Location

| Property | Value |
|----------|-------|
| **Database Type** | SQLite (Embedded) |
| **File Name** | `sourcematch.db` |
| **Location** | `c:\Users\2025\Desktop\sourcematch_project\sourcematch.db` |
| **Size** | ~88 KB |
| **Server Required** | ❌ No (embedded) |

---

## Current Database Contents

```
📊 TABLES AND RECORDS:
   • applications      → 3 records   (user job applications)
   • jobs              → 8 records   (job postings)
   • users             → 6 records   (registered users)
   • match_results     → 46 records  (scoring results)
   • match_searches    → 7 records   (resume uploads)
   • companies         → 0 records
   • blocks            → 0 records
```

---

## 🔓 How to Open & Browse Database

### **Method 1: DB Browser for SQLite (Easiest)**

1. **Download & Install:**
   - Visit: https://sqlitebrowser.org/
   - Download "DB Browser for SQLite"
   - Install on your Windows machine

2. **Open Database:**
   - Launch DB Browser
   - Click: **File → Open Database**
   - Navigate to: `c:\Users\2025\Desktop\sourcematch_project\sourcematch.db`
   - Click **Open**
   - Browse tables and data in GUI

**Pros:** Visual, user-friendly, no coding
**Cons:** Requires separate installation

---

### **Method 2: SQLite Command Line**

Open PowerShell and run:

```powershell
cd c:\Users\2025\Desktop\sourcematch_project
sqlite3 sourcematch.db
```

**Then execute SQL:**
```sql
-- View all tables
.tables

-- View users
SELECT * FROM users;

-- View jobs
SELECT * FROM jobs;

-- Count records
SELECT COUNT(*) FROM applications;

-- Exit
.quit
```

**Pros:** No installation needed, quick commands
**Cons:** Text interface

---

### **Method 3: Using Python Script**

Run provided script:

```powershell
cd c:\Users\2025\Desktop\sourcematch_project
.\venv\Scripts\Activate.ps1
python view_database.py
```

**Shows:** Database overview, table counts, file info

---

### **Method 4: VS Code SQLite Extension**

1. Install VS Code extension: **SQLite** (by alexcvzz)
2. Right-click `sourcematch.db` file
3. Select **"Open Database"**
4. Browse schema and data in sidebar

**Pros:** Built-in to editor
**Cons:** Limited functionality

---

## 📋 Database Tables Explained

### **users** - Registered users
```
Columns: id, email, password_hash, role, full_name, created_at
Current: 6 users (test accounts + registered users)
```

### **jobs** - Job postings
```
Columns: id, recruiter_id, company_id, title, description, requirements, created_at
Current: 8 sample jobs (Senior Python Dev, React Dev, Full Stack, etc.)
```

### **applications** - Job applications
```
Columns: id, job_id, candidate_id, resume_path, resume_text, score, status, explanation
Current: 3 applications submitted
```

### **match_searches** - Resume scoring searches
```
Columns: id, candidate_id, resume_path, fingerprint, created_at
Current: 7 resume uploads scored
```

### **match_results** - Scoring results
```
Columns: id, search_id, job_id, job_title, score, explanation, matched_skills
Current: 46 match results from scoring
```

---

## 🔄 Connection String (For Code)

**Located in:** `backend/models.py`

```python
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sourcematch.db")
```

**To change database:**
- PostgreSQL: `postgresql://user:password@localhost:5432/sourcematch`
- MySQL: `mysql+pymysql://user:password@localhost:3306/sourcematch`
- SQLite (current): `sqlite:///./sourcematch.db`

---

## 🛠️ Common Database Operations

### **Backup Database**
```powershell
Copy-Item sourcematch.db sourcematch_backup.db
```

### **Reset Database**
```powershell
Remove-Item sourcematch.db
# Restart backend - new database auto-created
python run_backend.py
```

### **Export Data to CSV**
Using DB Browser SQLite:
1. Open database
2. Right-click table
3. Select "Export as CSV"

### **Clear All Data**
```sql
-- Delete all records (keeps structure)
DELETE FROM users;
DELETE FROM jobs;
DELETE FROM applications;
DELETE FROM match_searches;
DELETE FROM match_results;
```

---

## 📌 Key Points

- ✅ **No server needed** - SQLite is embedded
- ✅ **Auto-initializes** - Tables created on first run
- ✅ **Persists data** - Survives app restarts
- ✅ **Easy to backup** - Just copy the file
- ⚠️ **Single user** - Not for multi-user production
- ⚠️ **File-based** - Not networked

---

## 📊 Useful SQL Queries

### View all users with roles
```sql
SELECT id, email, full_name, role, created_at FROM users;
```

### View all jobs
```sql
SELECT id, title, description FROM jobs;
```

### View job applications with details
```sql
SELECT 
  a.id, 
  u.full_name, 
  j.title, 
  ROUND(a.score * 100, 1) as score_percent,
  a.status
FROM applications a
JOIN users u ON a.candidate_id = u.id
JOIN jobs j ON a.job_id = j.id;
```

### View scoring history
```sql
SELECT 
  ms.created_at,
  mr.job_title,
  ROUND(mr.score * 100, 1) as score_percent,
  mr.matched_skills
FROM match_searches ms
JOIN match_results mr ON ms.id = mr.search_id
ORDER BY ms.created_at DESC
LIMIT 10;
```

### Get statistics
```sql
SELECT 
  (SELECT COUNT(*) FROM users) as total_users,
  (SELECT COUNT(*) FROM jobs) as total_jobs,
  (SELECT COUNT(*) FROM applications) as total_applications;
```

---

## 🚀 Next Steps

1. **Download DB Browser** → Browse data visually
2. **Run queries** → Execute SQL to analyze data
3. **Export data** → Backup to CSV
4. **Modify database** → Add/edit records directly

---

**For detailed guide, see:** `DATABASE_GUIDE.md`
