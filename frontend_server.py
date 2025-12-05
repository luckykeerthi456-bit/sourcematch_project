#!/usr/bin/env python3
"""
Simple standalone frontend server for SourceMatch.
Serves a static HTML+CSS+JS frontend without requiring Node.js or npm.
Make sure the backend is running on http://localhost:8000 before starting this.

Usage:
    python frontend_server.py
    
Then open http://localhost:3000 in your browser.
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 3000
FRONTEND_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SourceMatch - Explainable AI for Recruitment</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
                'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            background: #F8FAFF;
            color: #333;
        }
        
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: #6C5CE7;
            color: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        header h1 {
            font-size: 28px;
            margin: 0;
        }
        
        header div {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        button {
            background: #00B894;
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.2s;
        }
        
        button:hover {
            background: #00a085;
        }
        
        button.logout {
            background: white;
            color: #6C5CE7;
        }
        
        button.logout:hover {
            background: #f0f0f0;
        }
        
        .container {
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
        }
        
        .section {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 24px;
        }
        
        .section h2 {
            font-size: 20px;
            margin-bottom: 16px;
            color: #2c3e50;
        }
        
        .job-card {
            background: #f9f9f9;
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid #6C5CE7;
            margin-bottom: 12px;
        }
        
        .job-card h3 {
            margin: 0 0 8px 0;
            color: #2c3e50;
        }
        
        .job-card p {
            margin: 0;
            color: #666;
            font-size: 14px;
        }
        
        .job-card .apply-btn {
            margin-top: 12px;
            width: 100%;
        }
        
        .auth-buttons {
            display: flex;
            gap: 8px;
        }
        
        .auth-buttons button {
            flex: 1;
        }
        
        .auth-buttons button.candidate {
            background: #00B894;
        }
        
        .auth-buttons button.recruiter {
            background: #A29BFE;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        
        .modal.active {
            display: flex;
        }
        
        .modal-content {
            background: white;
            padding: 32px;
            border-radius: 12px;
            max-width: 500px;
            width: 90%;
        }
        
        .modal-content h2 {
            margin-bottom: 16px;
        }
        
        .form-group {
            margin-bottom: 12px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 4px;
            font-weight: 500;
            color: #2c3e50;
        }
        
        .form-group input,
        .form-group textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-family: inherit;
        }
        
        .form-group textarea {
            resize: vertical;
            min-height: 100px;
        }
        
        .modal-buttons {
            display: flex;
            gap: 8px;
            margin-top: 20px;
        }
        
        .modal-buttons button {
            flex: 1;
        }
        
        .message {
            padding: 12px 16px;
            border-radius: 6px;
            margin-bottom: 16px;
            display: none;
        }
        
        .message.show {
            display: block;
        }
        
        .message.success {
            background: #D4EDDA;
            color: #155724;
            border: 1px solid #C3E6CB;
        }
        
        .message.error {
            background: #F8D7DA;
            color: #721C24;
            border: 1px solid #F5C6CB;
        }
        
        .loading {
            display: inline-block;
            opacity: 0.6;
        }
        
        .empty {
            text-align: center;
            padding: 40px;
            color: #999;
        }
    </style>
</head>
<body>
    <header>
        <h1>SourceMatch</h1>
        <div id="userInfo">
            <span>Not signed in</span>
        </div>
    </header>
    
    <div class="container">
        <div id="message" class="message"></div>
        
        <div id="authSection" class="section">
            <h2>Get Started</h2>
            <p style="margin-bottom: 16px; color: #666;">Sign in to apply for jobs or post them.</p>
            <div class="auth-buttons">
                <button class="candidate" onclick="mockRegister('candidate')">Sign in as Candidate</button>
                <button class="recruiter" onclick="mockRegister('recruiter')">Sign in as Recruiter</button>
            </div>
        </div>
        
        <div id="jobsSection" class="section" style="display: none;">
            <h2>Available Jobs</h2>
            <div id="jobsList" class="empty">Loading jobs...</div>
        </div>
    </div>
    
    <div id="applyModal" class="modal">
        <div class="modal-content">
            <h2 id="applyJobTitle"></h2>
            <form onsubmit="submitApply(event)">
                <div class="form-group">
                    <label>Upload Resume (PDF or TXT)</label>
                    <input type="file" id="resumeFile" accept=".pdf,.txt" required>
                </div>
                <div class="modal-buttons">
                    <button type="submit">Submit Application</button>
                    <button type="button" onclick="closeApplyModal()" style="background: #999;">Cancel</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        const API = "http://localhost:8000/api";
        let user = null;
        let jobs = [];
        let selectedJob = null;
        
        // Show message helper
        function showMessage(text, isError = false) {
            const msgEl = document.getElementById("message");
            msgEl.textContent = text;
            msgEl.className = "message show " + (isError ? "error" : "success");
            setTimeout(() => msgEl.classList.remove("show"), 5000);
        }
        
        // Fetch jobs from backend
        async function fetchJobs() {
            try {
                const res = await fetch(API + "/jobs/");
                jobs = await res.json();
                renderJobs();
            } catch (err) {
                console.error(err);
                showMessage("Failed to fetch jobs. Make sure backend is running on http://localhost:8000", true);
            }
        }
        
        // Render jobs list
        function renderJobs() {
            const jobsList = document.getElementById("jobsList");
            if (!jobs.length) {
                jobsList.innerHTML = '<p class="empty">No jobs available. (Create one via the backend API)</p>';
                return;
            }
            jobsList.innerHTML = jobs.map(job => `
                <div class="job-card">
                    <h3>${job.title}</h3>
                    <p>${job.description}</p>
                    <button class="apply-btn" onclick="openApplyModal(${job.id}, '${job.title}')">Apply Now</button>
                </div>
            `).join("");
        }
        
        // Mock register
        async function mockRegister(role) {
            const email = role === "candidate" ? "alice@example.com" : "recruiter@example.com";
            const fullName = role === "candidate" ? "Alice Candidate" : "Ravi Recruiter";
            
            try {
                // Try register first
                await fetch(API + "/users/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password: "password", role, full_name: fullName })
                }).catch(() => {}); // Ignore if user already exists
                
                // Login
                const loginRes = await fetch(API + "/users/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password: "password" })
                });
                
                const loginData = await loginRes.json();
                user = loginData.user;
                const token = loginData.access_token;
                
                // Update UI
                updateUserDisplay();
                document.getElementById("authSection").style.display = "none";
                document.getElementById("jobsSection").style.display = "block";
                fetchJobs();
                showMessage("Signed in as " + user.email);
                
            } catch (err) {
                console.error(err);
                showMessage("Sign in failed: " + err.message, true);
            }
        }
        
        // Update user display
        function updateUserDisplay() {
            const userInfo = document.getElementById("userInfo");
            if (user) {
                userInfo.innerHTML = `
                    <span>${user.full_name} (${user.role})</span>
                    <button class="logout" onclick="logout()">Logout</button>
                `;
            } else {
                userInfo.innerHTML = '<span>Not signed in</span>';
            }
        }
        
        // Logout
        function logout() {
            user = null;
            updateUserDisplay();
            document.getElementById("authSection").style.display = "block";
            document.getElementById("jobsSection").style.display = "none";
            showMessage("Logged out");
        }
        
        // Open apply modal
        function openApplyModal(jobId, jobTitle) {
            if (!user) {
                showMessage("Please sign in as a candidate to apply", true);
                return;
            }
            selectedJob = jobs.find(j => j.id === jobId);
            document.getElementById("applyJobTitle").textContent = "Apply for: " + jobTitle;
            document.getElementById("applyModal").classList.add("active");
        }
        
        // Close apply modal
        function closeApplyModal() {
            document.getElementById("applyModal").classList.remove("active");
            document.getElementById("resumeFile").value = "";
        }
        
        // Submit application
        async function submitApply(e) {
            e.preventDefault();
            
            if (!selectedJob) {
                showMessage("No job selected", true);
                return;
            }
            
            const resumeFile = document.getElementById("resumeFile").files[0];
            if (!resumeFile) {
                showMessage("Please select a resume file", true);
                return;
            }
            
            try {
                const fd = new FormData();
                fd.append("job_id", selectedJob.id);
                fd.append("candidate_id", user.id);
                fd.append("resume", resumeFile);
                
                const res = await fetch(API + "/applications/apply", {
                    method: "POST",
                    body: fd
                });
                
                if (!res.ok) {
                    throw new Error("Application failed: " + await res.text());
                }
                
                const data = await res.json();
                showMessage("Application submitted! ID: " + data.application_id);
                closeApplyModal();
                
            } catch (err) {
                console.error(err);
                showMessage("Failed to submit application: " + err.message, true);
            }
        }
        
        // Initialize
        window.addEventListener("load", () => {
            updateUserDisplay();
        });
    </script>
</body>
</html>
"""

class FrontendHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the HTML for all paths (SPA behavior)
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(FRONTEND_HTML.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == "__main__":
    handler = FrontendHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"✓ SourceMatch Frontend running on http://localhost:{PORT}")
        print(f"✓ Make sure backend is running on http://localhost:8000")
        print(f"✓ Press Ctrl+C to stop the server")
        print()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✓ Server stopped")
