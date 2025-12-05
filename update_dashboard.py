#!/usr/bin/env python3
"""
Create comprehensive Dashboard component with resume scorer and job finder
"""
import os
from pathlib import Path

frontend_src = Path("c:/Users/2025/Desktop/sourcematch_project/frontend/src")

dashboard_code = '''import React, { useState, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:8000/api";

export default function Dashboard({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState("home");
  const [jobs, setJobs] = useState([]);
  const [resumeFile, setResumeFile] = useState(null);
  const [scoring, setScoring] = useState(null);
  const [loadingScore, setLoadingScore] = useState(false);
  const [loadingJobs, setLoadingJobs] = useState(false);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [message, setMessage] = useState("");

  // Load jobs when tab changes
  useEffect(() => {
    if (activeTab === "jobs") {
      fetchJobs();
    }
  }, [activeTab]);

  const fetchJobs = async () => {
    setLoadingJobs(true);
    try {
      const res = await axios.get(API + "/jobs");
      setJobs(res.data || []);
    } catch (err) {
      setMessage("Failed to load jobs");
    } finally {
      setLoadingJobs(false);
    }
  };

  const handleResumeUpload = async (e) => {
    e.preventDefault();
    if (!resumeFile) {
      setMessage("Please select a resume file");
      return;
    }

    setLoadingScore(true);
    setMessage("");

    const formData = new FormData();
    formData.append("resume", resumeFile);

    try {
      const res = await axios.post(API + "/applications/score", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setScoring(res.data);
      setMessage("Resume scored successfully!");
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Failed to score resume");
    } finally {
      setLoadingScore(false);
    }
  };

  const handleApply = async (jobId) => {
    try {
      await axios.post(API + "/applications/apply", {
        job_id: jobId,
        resume_text: resumeFile ? "uploaded" : "",
      });
      setMessage("Applied successfully!");
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Failed to apply");
    }
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", background: "#F8FAFF", minHeight: "100vh" }}>
      {/* Header */}
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: 20,
          background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
          color: "#fff",
          boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
        }}
      >
        <div>
          <h1 style={{ margin: "0 0 4px 0" }}>SourceMatch</h1>
          <p style={{ margin: 0, fontSize: 12, opacity: 0.9 }}>AI-Powered Job Matching</p>
        </div>
        <div style={{ textAlign: "right" }}>
          <p style={{ margin: "0 0 8px 0", fontSize: 14 }}>
            {user.full_name} • {user.role === "candidate" ? "👤 Job Seeker" : "👔 Recruiter"}
          </p>
          <button
            onClick={onLogout}
            style={{
              background: "#fff",
              color: "#667eea",
              border: "none",
              padding: "8px 16px",
              borderRadius: 6,
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            Logout
          </button>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div
        style={{
          background: "#fff",
          borderBottom: "2px solid #e5e7eb",
          display: "flex",
          gap: 0,
        }}
      >
        {[
          { id: "home", label: "🏠 Home", show: true },
          { id: "scorer", label: "📄 Resume Scorer", show: true },
          { id: "jobs", label: "💼 Job Finder", show: true },
          { id: "history", label: "📋 History", show: true },
        ].map(
          (tab) =>
            tab.show && (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  padding: "16px 24px",
                  border: "none",
                  background: activeTab === tab.id ? "#667eea" : "transparent",
                  color: activeTab === tab.id ? "#fff" : "#6b7280",
                  cursor: "pointer",
                  fontWeight: 600,
                  fontSize: 14,
                  transition: "all 0.3s",
                }}
              >
                {tab.label}
              </button>
            )
        )}
      </div>

      {/* Main Content */}
      <main style={{ maxWidth: 1200, margin: "0 auto", padding: "24px" }}>
        {message && (
          <div
            style={{
              padding: 12,
              marginBottom: 16,
              background: message.includes("successfully") ? "#d1fae5" : "#fee2e2",
              color: message.includes("successfully") ? "#065f46" : "#991b1b",
              borderRadius: 8,
              fontSize: 14,
            }}
          >
            {message}
          </div>
        )}

        {/* HOME TAB */}
        {activeTab === "home" && (
          <div>
            <h2>Welcome, {user.full_name}! 👋</h2>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
                gap: 20,
                marginTop: 24,
              }}
            >
              {/* Card 1: Resume Scorer */}
              <div
                onClick={() => setActiveTab("scorer")}
                style={{
                  background: "#fff",
                  padding: 24,
                  borderRadius: 12,
                  boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                  cursor: "pointer",
                  transition: "transform 0.2s, box-shadow 0.2s",
                  border: "2px solid transparent",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-4px)";
                  e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow = "0 2px 8px rgba(0,0,0,0.08)";
                }}
              >
                <h3 style={{ margin: "0 0 12px 0", color: "#667eea" }}>📄 Resume Scorer</h3>
                <p style={{ margin: 0, color: "#6b7280", lineHeight: 1.6 }}>
                  Upload your resume and get AI-powered scoring against available jobs. Get detailed
                  feedback on skill matches and recommendations.
                </p>
              </div>

              {/* Card 2: Job Finder */}
              <div
                onClick={() => setActiveTab("jobs")}
                style={{
                  background: "#fff",
                  padding: 24,
                  borderRadius: 12,
                  boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                  cursor: "pointer",
                  transition: "transform 0.2s, box-shadow 0.2s",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-4px)";
                  e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow = "0 2px 8px rgba(0,0,0,0.08)";
                }}
              >
                <h3 style={{ margin: "0 0 12px 0", color: "#667eea" }}>💼 Job Finder</h3>
                <p style={{ margin: 0, color: "#6b7280", lineHeight: 1.6 }}>
                  Browse available job positions, filter by skills and experience level, and apply to
                  positions that match your profile.
                </p>
              </div>

              {/* Card 3: Search History */}
              <div
                onClick={() => setActiveTab("history")}
                style={{
                  background: "#fff",
                  padding: 24,
                  borderRadius: 12,
                  boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                  cursor: "pointer",
                  transition: "transform 0.2s, box-shadow 0.2s",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-4px)";
                  e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow = "0 2px 8px rgba(0,0,0,0.08)";
                }}
              >
                <h3 style={{ margin: "0 0 12px 0", color: "#667eea" }}>📋 Search History</h3>
                <p style={{ margin: 0, color: "#6b7280", lineHeight: 1.6 }}>
                  View all your past resume scoring searches, see which jobs matched best, and track
                  your application history.
                </p>
              </div>
            </div>

            {/* User Info Box */}
            <div
              style={{
                background: "#fff",
                padding: 24,
                borderRadius: 12,
                boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                marginTop: 24,
              }}
            >
              <h3 style={{ margin: "0 0 16px 0" }}>Your Profile</h3>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
                <div>
                  <strong style={{ color: "#6b7280" }}>Email:</strong>
                  <p style={{ margin: "4px 0 0 0" }}>{user.email}</p>
                </div>
                <div>
                  <strong style={{ color: "#6b7280" }}>Role:</strong>
                  <p style={{ margin: "4px 0 0 0" }}>
                    {user.role === "candidate" ? "Job Seeker" : "Recruiter"}
                  </p>
                </div>
                <div>
                  <strong style={{ color: "#6b7280" }}>Name:</strong>
                  <p style={{ margin: "4px 0 0 0" }}>{user.full_name}</p>
                </div>
                <div>
                  <strong style={{ color: "#6b7280" }}>Member Since:</strong>
                  <p style={{ margin: "4px 0 0 0" }}>Today</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* RESUME SCORER TAB */}
        {activeTab === "scorer" && (
          <div>
            <h2>📄 Resume Scorer</h2>
            <div
              style={{
                background: "#fff",
                padding: 24,
                borderRadius: 12,
                boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              }}
            >
              <form onSubmit={handleResumeUpload}>
                <div
                  style={{
                    border: "2px dashed #667eea",
                    borderRadius: 8,
                    padding: 40,
                    textAlign: "center",
                    cursor: "pointer",
                    transition: "all 0.3s",
                    background: "#f8f9ff",
                  }}
                  onClick={() => document.getElementById("resumeInput").click()}
                >
                  <p style={{ fontSize: 24, margin: "0 0 8px 0" }}>📤</p>
                  <p style={{ margin: "0 0 4px 0", fontWeight: 600 }}>
                    Click to upload or drag your resume
                  </p>
                  <p style={{ margin: 0, color: "#6b7280", fontSize: 12 }}>
                    PDF files only, max 10MB
                  </p>
                  <input
                    id="resumeInput"
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setResumeFile(e.target.files?.[0])}
                    style={{ display: "none" }}
                  />
                </div>

                {resumeFile && (
                  <div style={{ marginTop: 16, padding: 12, background: "#f0f9ff", borderRadius: 8 }}>
                    <p style={{ margin: 0, fontSize: 14 }}>
                      ✅ Selected: <strong>{resumeFile.name}</strong>
                    </p>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={!resumeFile || loadingScore}
                  style={{
                    marginTop: 20,
                    width: "100%",
                    padding: 12,
                    background: resumeFile && !loadingScore ? "#667eea" : "#d1d5db",
                    color: "#fff",
                    border: "none",
                    borderRadius: 8,
                    fontWeight: 600,
                    cursor: resumeFile && !loadingScore ? "pointer" : "not-allowed",
                  }}
                >
                  {loadingScore ? "Scoring..." : "Score Resume"}
                </button>
              </form>

              {scoring && (
                <div style={{ marginTop: 24 }}>
                  <h3>📊 Scoring Results</h3>
                  <div style={{ display: "grid", gap: 16 }}>
                    {scoring.matches &&
                      scoring.matches.slice(0, 5).map((match, idx) => (
                        <div
                          key={idx}
                          style={{
                            background: "#f9fafb",
                            padding: 16,
                            borderRadius: 8,
                            border: "1px solid #e5e7eb",
                          }}
                        >
                          <div style={{ display: "flex", justifyContent: "space-between" }}>
                            <div>
                              <h4 style={{ margin: "0 0 4px 0" }}>{match.job?.title}</h4>
                              <p style={{ margin: 0, color: "#6b7280", fontSize: 14 }}>
                                {match.job?.company}
                              </p>
                            </div>
                            <div style={{ textAlign: "right" }}>
                              <p style={{ margin: 0, fontSize: 20, fontWeight: 600, color: "#667eea" }}>
                                {Math.round(match.score * 100)}%
                              </p>
                              <p style={{ margin: 0, fontSize: 12, color: "#6b7280" }}>Match Score</p>
                            </div>
                          </div>
                          {match.explanation && (
                            <div style={{ marginTop: 12 }}>
                              <p style={{ margin: 0, fontSize: 12, color: "#374151" }}>
                                {match.explanation.summary || "Good match"}
                              </p>
                            </div>
                          )}
                        </div>
                      ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* JOB FINDER TAB */}
        {activeTab === "jobs" && (
          <div>
            <h2>💼 Job Finder</h2>
            {loadingJobs ? (
              <p>Loading jobs...</p>
            ) : (
              <div style={{ display: "grid", gap: 16 }}>
                {jobs && jobs.length > 0 ? (
                  jobs.map((job) => (
                    <div
                      key={job.id}
                      style={{
                        background: "#fff",
                        padding: 24,
                        borderRadius: 12,
                        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                      }}
                    >
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}>
                        <div style={{ flex: 1 }}>
                          <h3 style={{ margin: "0 0 4px 0" }}>{job.title}</h3>
                          <p style={{ margin: "0 0 12px 0", color: "#6b7280" }}>
                            {job.company} • {job.location}
                          </p>
                          <p style={{ margin: "0 0 12px 0", color: "#374151", lineHeight: 1.6 }}>
                            {job.description}
                          </p>
                          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                            {job.required_skills &&
                              job.required_skills.split(",").map((skill, idx) => (
                                <span
                                  key={idx}
                                  style={{
                                    background: "#e0e7ff",
                                    color: "#667eea",
                                    padding: "4px 8px",
                                    borderRadius: 4,
                                    fontSize: 12,
                                    fontWeight: 500,
                                  }}
                                >
                                  {skill.trim()}
                                </span>
                              ))}
                          </div>
                        </div>
                        <div style={{ marginLeft: 20, textAlign: "right" }}>
                          <p style={{ margin: "0 0 4px 0", fontWeight: 600 }}>
                            {job.salary_min ? `$${job.salary_min}K` : "Negotiable"}
                          </p>
                          <p style={{ margin: "0 0 12px 0", color: "#6b7280", fontSize: 14 }}>
                            {job.experience_level} exp
                          </p>
                          <button
                            onClick={() => handleApply(job.id)}
                            style={{
                              padding: "8px 16px",
                              background: "#667eea",
                              color: "#fff",
                              border: "none",
                              borderRadius: 6,
                              cursor: "pointer",
                              fontWeight: 600,
                            }}
                          >
                            Apply
                          </button>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <p>No jobs available yet. Check back soon!</p>
                )}
              </div>
            )}
          </div>
        )}

        {/* HISTORY TAB */}
        {activeTab === "history" && (
          <div>
            <h2>📋 Search History</h2>
            <div
              style={{
                background: "#fff",
                padding: 24,
                borderRadius: 12,
                boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                textAlign: "center",
              }}
            >
              <p style={{ color: "#6b7280" }}>
                Your search history will appear here when you score resumes.
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
'''

# Write the dashboard file
with open(frontend_src / "Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(dashboard_code)

print("✅ Dashboard.jsx updated with Resume Scorer, Job Finder, and all features!")
