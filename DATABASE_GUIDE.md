# SourceMatch Database Guide

## 📊 Database Type

**Database Used:** **SQLite**

- **File Location:** `sourcematch.db` (in project root)
- **Type:** Embedded relational database (no server needed)
- **Perfect for:** Development, prototyping, and small-scale applications

---

## 📁 Database File Location

```
c:\Users\2025\Desktop\sourcematch_project\sourcematch.db
```

---

## 🔓 How to Open & Browse the Database

### **Option 1: Using DB Browser for SQLite (Recommended)**

**Download & Install:**
1. Go to: https://sqlitebrowser.org/
2. Download "DB Browser for SQLite"
3. Install on your machine

**Open the database:**
1. Launch DB Browser for SQLite
2. Click **File** → **Open Database**
3. Navigate to: `c:\Users\2025\Desktop\sourcematch_project\sourcematch.db`
4. Click **Open**
5. Browse tables, view data, run SQL queries

---

### **Option 2: Using Command Line (SQLite CLI)**

**If SQLite CLI is installed:**

```powershell
cd c:\Users\2025\Desktop\sourcematch_project
sqlite3 sourcematch.db
```

**Common SQLite commands:**
```sql
-- List all tables
.tables

-- View schema of a table
.schema users

-- View all data in a table
SELECT * FROM users;

-- View specific columns
SELECT id, email, full_name FROM users;

-- Count records
SELECT COUNT(*) FROM jobs;

-- Exit
.quit
```

---

### **Option 3: Using Python Script**

Create a script to view database contents:

```python
import sqlite3

# Connect to database
conn = sqlite3.connect('sourcematch.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in database:")
for table in tables:
    print(f"  - {table[0]}")
    cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5;")
    rows = cursor.fetchall()
    print(f"    Records: {len(rows)}")

conn.close()
```

Run:
```powershell
python view_db.py
```

---

### **Option 4: Using VS Code SQLite Extension**

1. Open VS Code
2. Install extension: **"SQLite"** by alexcvzz
3. Right-click `sourcematch.db` → **"Open Database"**
4. See schema and data in sidebar

---

## 📋 Database Tables & Schema

### **1. users**
Stores user account information
```sql
id (Primary Key)
email (Unique)
password_hash
role (candidate/recruiter)
full_name
created_at
```

**Records:** All registered users

---

### **2. companies**
Stores company information
```sql
id (Primary Key)
name
```

**Records:** Companies hiring

---

### **3. jobs**
Stores job postings
```sql
id (Primary Key)
recruiter_id (Foreign Key → users.id)
company_id (Foreign Key → companies.id)
title
description (Text)
requirements (JSON)
created_at
```

**Records:** Currently **8 sample jobs**

---

### **4. applications**
Stores job applications
```sql
id (Primary Key)
job_id (Foreign Key → jobs.id)
candidate_id (Foreign Key → users.id)
resume_path
resume_text
score (Float, 0-1)
status (applied/shortlisted/rejected)
explanation (JSON)
fingerprint
```

**Records:** User applications to jobs

---

### **5. match_search**
Stores resume scoring searches
```sql
id (Primary Key)
candidate_id (Foreign Key → users.id)
resume_path
fingerprint
created_at
```

**Records:** Each resume upload

---

### **6. match_result**
Stores scoring results for each search
```sql
id (Primary Key)
search_id (Foreign Key → match_search.id)
job_id (Foreign Key → jobs.id)
job_title
score (Float, 0-1)
explanation (JSON)
matched_skills (JSON Array)
```

**Records:** Each match for every search

---

## 📊 Quick Database Queries

### **View All Users**
```sql
SELECT id, email, full_name, role, created_at FROM users;
```

### **View All Jobs**
```sql
SELECT id, title, description, requirements FROM jobs LIMIT 10;
```

### **View Job Applications**
```sql
SELECT a.id, u.full_name, j.title, a.score, a.status 
FROM applications a
JOIN users u ON a.candidate_id = u.id
JOIN jobs j ON a.job_id = j.id;
```

### **View Resume Scoring History**
```sql
SELECT ms.id, ms.candidate_id, mr.job_title, mr.score, mr.created_at
FROM match_search ms
JOIN match_result mr ON ms.id = mr.search_id
ORDER BY ms.created_at DESC;
```

### **Count Records**
```sql
SELECT 
  (SELECT COUNT(*) FROM users) as total_users,
  (SELECT COUNT(*) FROM jobs) as total_jobs,
  (SELECT COUNT(*) FROM applications) as total_applications,
  (SELECT COUNT(*) FROM match_search) as total_searches;
```

---

## 🔄 Database Connection in Code

**Backend connection string:**
```python
# Located in: backend/models.py
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sourcematch.db")
```

**Change database:**
- For PostgreSQL: `postgresql://user:password@localhost:5432/sourcematch`
- For MySQL: `mysql+pymysql://user:password@localhost:3306/sourcematch`
- Current (SQLite): `sqlite:///./sourcematch.db`

---

## 🛠️ Database Maintenance

### **Reset Database**
```powershell
# Delete the database file
Remove-Item sourcematch.db

# Restart backend to auto-create new database
python run_backend.py
```

### **Backup Database**
```powershell
# Copy database file
Copy-Item sourcematch.db sourcematch_backup.db
```

### **Export Data to CSV**
Use DB Browser SQLite → Export as CSV

---

## 📌 Important Notes

- ✅ **No database server required** - SQLite is embedded
- ✅ **Automatic initialization** - Tables created on first run
- ✅ **Data persists** - Survives application restarts
- ✅ **Can be version controlled** - Add to Git if needed
- ⚠️ **Not suitable for high-concurrency** - Consider PostgreSQL for production
- ⚠️ **Limited to single machine** - Not networked

---

## 🚀 For Production

**Recommended upgrade:**
```
SQLite (Development) → PostgreSQL (Production)
```

Change in `backend/models.py`:
```python
DATABASE_URL = "postgresql://user:password@hostname:5432/sourcematch"
```

---

**Database location:** `c:\Users\2025\Desktop\sourcematch_project\sourcematch.db`

Happy data exploring! 🎯
