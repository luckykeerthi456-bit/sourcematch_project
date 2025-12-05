# Recruiter Portal - Quick Access Guide

## 🎯 How to Access the Recruiter Portal

### Method 1: Register as a Recruiter (First Time)

```
1. Open http://localhost:3000
         ↓
2. Click "Register" tab
         ↓
3. Fill in the form:
   - Full Name: [Your Name]
   - Email: [your-email@example.com]
   - Password: [YourPassword123]
   - Role: SELECT "recruiter" ← IMPORTANT!
         ↓
4. Click "Register" button
         ↓
5. ✅ Automatically logged in to Recruiter Portal
```

### Method 2: Login with Existing Recruiter Account

```
1. Open http://localhost:3000
         ↓
2. Click "Login" tab
         ↓
3. Enter credentials:
   - Email: [recruiter@example.com]
   - Password: [YourPassword123]
         ↓
4. Click "Login" button
         ↓
5. ✅ Directed to Recruiter Portal (if role = recruiter)
```

---

## 📋 Recruiter Portal Features

### Navigation Bar
```
┌─────────────────────────────────────────────────────┐
│  SourceMatch - Recruiter Portal                   │
│  Manage Applications & Review Candidates           │
│                                           [Logout] │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  📋 Applications  │  📊 Statistics                   │
└─────────────────────────────────────────────────────┘
```

### Applications Tab (Default)

#### Filter Bar
```
[All] [Applied] [Shortlisted] [Rejected]
```

#### Application List
```
┌─ Application Card ────────────────────────────┐
│  Candidate Name                               │
│  Applied for: Job Title                       │
│  candidate@email.com                          │
│                        Score: 48%  [Status]  │
└───────────────────────────────────────────────┘
```

#### Click to View Details
```
┌─ Candidate Profile ─────────┐  ┌─ Resume & Actions ─────┐
│                             │  │                        │
│ Full Name: John Doe         │  │ Resume Preview:        │
│ Email: john@email.com       │  │ (Full resume text)     │
│ Applied for: Senior Dev     │  │ ...                    │
│                             │  │ ...                    │
│ Match Score: 85%            │  │ [✓ Shortlist] [✗ Deny]│
│ Skills: Python, AWS, React  │  │ [📧 Send Email]        │
│ Date: Dec 5, 2025           │  │                        │
│                             │  │ Status: Shortlisted    │
└─────────────────────────────┘  └────────────────────────┘
```

### Statistics Tab

```
┌─────────────────────────────────────────┐
│  Total Applications: 15                 │
│  Shortlisted: 5 (green)                 │
│  Rejected: 3 (red)                      │
│  Pending Review: 7 (orange)             │
└─────────────────────────────────────────┘

┌─ Top 5 Matches ─────────────────────────┐
│  1. John Doe - 85%                      │
│  2. Jane Smith - 78%                    │
│  3. Bob Johnson - 75%                   │
│  4. Alice Brown - 72%                   │
│  5. Charlie Davis - 68%                 │
└─────────────────────────────────────────┘
```

---

## 🎮 Actions Available

### Shortlist a Candidate
```
1. Click on application in list
         ↓
2. Click [✓ Shortlist] button
         ↓
3. ✅ Status changed to "Shortlisted"
4. ✅ Appears in Shortlisted filter
5. ✅ Statistics updated automatically
```

### Reject a Candidate
```
1. Click on application in list
         ↓
2. Click [✗ Reject] button
         ↓
3. ✅ Status changed to "Rejected"
4. ✅ Appears in Rejected filter
5. ✅ Statistics updated automatically
```

### Send Email to Candidate
```
1. Click on application in list
         ↓
2. Click [📧 Send Email] button
         ↓
3. ✅ Opens your default email client
4. ✅ Pre-filled with candidate's email
5. ✅ Compose and send message
```

### View Resume
```
1. Click on application in list
         ↓
2. Resume preview shown on right side
         ↓
3. ✅ Scroll to read full resume
4. ✅ See all candidate text
```

### Check Match Score
```
Application List:
- Shows percentage (e.g., 48%)

Application Details:
- Shows percentage (e.g., 85%)
- Shows progress bar
- Shows matched skills

Score Calculation:
- Semantic Similarity (40%)
- Skill Match (35%)
- Experience Match (25%)
```

---

## 📊 Understanding the Scores

### Score Breakdown

| Component | Weight | Example |
|-----------|--------|---------|
| Semantic Similarity | 40% | 0.95 × 0.40 = 0.38 |
| Skill Match | 35% | 0.85 × 0.35 = 0.30 |
| Experience Match | 25% | 0.80 × 0.25 = 0.20 |
| **Total Score** | **100%** | **0.88 = 88%** |

### Score Interpretation

```
90-100%  ⭐⭐⭐⭐⭐ Excellent Match
75-89%   ⭐⭐⭐⭐   Very Good Match
60-74%   ⭐⭐⭐     Good Match
45-59%   ⭐⭐       Fair Match
0-44%    ⭐        Poor Match
```

---

## 🔄 Application Status Flow

```
┌─────────────┐
│   Applied   │  (Initial status when candidate submits)
└──────┬──────┘
       │
       ├─→ [✓ Shortlist] → ┌──────────────┐
       │                   │ Shortlisted  │ (Approved for next round)
       │                   └──────────────┘
       │
       └─→ [✗ Reject] ──→ ┌──────────┐
                          │ Rejected │ (Not suitable)
                          └──────────┘
```

---

## 📈 Filter Applications

### By Status
```
[All]          → Show all applications
[Applied]      → Show pending review (yellow)
[Shortlisted]  → Show approved (green)
[Rejected]     → Show declined (red)
```

### By Score (Manual)
1. View applications list
2. Look at score % for each
3. Click to view details
4. Statistics tab shows top matches

---

## 💡 Tips & Tricks

### Best Practices
1. **Start with highest scores**: Focus on 75%+ matches first
2. **Check matched skills**: Verify required skills are present
3. **Review resume text**: Ensure quality and relevance
4. **Send timely responses**: Contact candidates quickly
5. **Track statistics**: Monitor your review progress

### Keyboard Shortcuts
- No keyboard shortcuts yet (future feature)

### Bulk Actions (Coming Soon)
- [ ] Shortlist multiple candidates
- [ ] Send bulk emails
- [ ] Export to CSV/PDF

---

## ⚙️ Settings & Preferences (Future)

### Upcoming Features
- [ ] Email templates
- [ ] Auto-reply options
- [ ] Notification preferences
- [ ] Custom scoring weights
- [ ] Interview scheduling

---

## 🆘 Troubleshooting

### Problem: Can't see Recruiter Portal
**Solution**: 
1. Make sure you registered with `role = "recruiter"`
2. Check browser console (F12) for errors
3. Verify backend is running (port 8001)

### Problem: Applications not loading
**Solution**:
1. Refresh the page
2. Check network tab (F12) for API errors
3. Restart backend

### Problem: Can't update status
**Solution**:
1. Make sure application exists
2. Click button and wait for response
3. Check for error message
4. Refresh and try again

### Problem: Can't send email
**Solution**:
1. Button opens your default email client
2. If not working, copy candidate email manually
3. Open your email provider directly

---

## 📞 Contact & Support

### For Technical Issues
1. Check `RECRUITER_PORTAL_GUIDE.md` (full documentation)
2. Run `test_recruiter_portal.py` (verify endpoints)
3. Check browser console errors
4. Check backend logs

### For Feature Requests
- Email: support@sourcematch.com
- Status: 🟢 Production Ready

---

## 🎓 Quick Training

### Training Scenario: Review Your First Application

```
Time Required: 2-3 minutes

Step 1: Login (30 seconds)
└─ Use recruiter credentials

Step 2: View Applications (30 seconds)
└─ See list of all applications

Step 3: Select Application (1 minute)
└─ Click on any application card

Step 4: Review Details (1 minute)
└─ Check candidate info
└─ Review resume
└─ Check match score

Step 5: Make Decision (30 seconds)
└─ Click Shortlist or Reject
└─ See status change

Step 6: Verify (30 seconds)
└─ Go back to list
└─ See updated status
```

### Training Scenario: Send Email to Candidate

```
Time Required: 1-2 minutes

Step 1: Select Application (30 seconds)
└─ Click on candidate

Step 2: Click Send Email (30 seconds)
└─ Click [📧 Send Email] button

Step 3: Compose Message (1 minute)
└─ Your email client opens
└─ Candidate email is ready
└─ Write your message

Step 4: Send (30 seconds)
└─ Click Send in your email client
└─ Done!
```

---

## 📱 Browser Support

| Browser | Status |
|---------|--------|
| Chrome | ✅ Supported |
| Firefox | ✅ Supported |
| Safari | ✅ Supported |
| Edge | ✅ Supported |
| IE 11 | ❌ Not Supported |

---

## 🚀 Getting Started Checklist

- [ ] Backend running (port 8001)
- [ ] Frontend running (port 3000)
- [ ] Registered as recruiter
- [ ] Logged into recruiter portal
- [ ] Can see applications list
- [ ] Can view application details
- [ ] Can update application status
- [ ] Can send emails to candidates

**All checked? You're ready to start recruiting! 🎉**

---

Last Updated: December 5, 2025
