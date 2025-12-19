import React, { useState, useEffect } from "react";
import axios from "axios";
import Toast from "./components/Toast";

const API = "http://localhost:8000/api";

export default function Dashboard({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState("home");
  const [jobs, setJobs] = useState([]);
  const [resumeFile, setResumeFile] = useState(null);
  const [scoring, setScoring] = useState(null);
  const [loadingScore, setLoadingScore] = useState(false);
  const [loadingJobs, setLoadingJobs] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [history, setHistory] = useState([]);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [message, setMessage] = useState("");

  // Helper to robustly format scores as 0-100% even if backend scaling varies
  const formatPercent = (score) => {
    const s = Number(score) || 0;
    let perc = 0;
    if (s <= 1) {
      perc = s * 100;
    } else if (s > 1 && s <= 10) {
      // sometimes score was accidentally scaled by 10 (e.g. 8.85 -> 88.5)
      perc = s * 10;
    } else if (s > 10 && s <= 100) {
      // already a percentage
      perc = s;
    } else {
      // fallback: clamp
      perc = s;
    }
    perc = Math.max(0, Math.min(100, perc));
    return Math.round(perc);
  };

  // Load jobs or history when tab changes
  useEffect(() => {
    if (activeTab === "jobs") {
      fetchJobs();
    } else if (activeTab === "history") {
      fetchHistory();
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

  const fetchHistory = async () => {
    setLoadingHistory(true);
    try {
      const res = await axios.get(API + "/applications/history");
      console.log("History data:", res.data);
      setHistory(res.data || []);
    } catch (err) {
      console.error("History error:", err);
      setMessage("Failed to load history");
    } finally {
      setLoadingHistory(false);
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
      console.log("Backend response:", res.data);
      // Backend returns array of JobScore objects, wrap in {matches: [...]}
      setScoring({ matches: res.data || [] });
      setMessage("Resume scored successfully!");
    } catch (err) {
      console.error("Score error:", err);
      setMessage(err?.response?.data?.detail || "Failed to score resume");
    } finally {
      setLoadingScore(false);
    }
  };

  const handleApply = async (jobId) => {
    try {
      // Prepare FormData with job_id, candidate_id, and resume file
      const formData = new FormData();
      formData.append("job_id", jobId);
      formData.append("candidate_id", user.id);
      
      // If user has uploaded a resume, use it; otherwise create a placeholder file
      if (resumeFile) {
        formData.append("resume", resumeFile);
      } else {
        // Create a minimal text file as placeholder resume
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

  const deleteHistory = async (searchId) => {
    if (!window.confirm("Are you sure you want to delete this search history entry? This cannot be undone.")) return;
    try {
      await axios.delete(API + `/applications/history/${searchId}`);
      setMessage("History entry deleted");
      await fetchHistory();
    } catch (err) {
      console.error("Failed to delete history:", err);
      setMessage(err?.response?.data?.detail || "Failed to delete history");
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
        {/* Toast area (auto-dismiss) */}
        {message && (
          <Toast
            message={message}
            onClose={() => setMessage("")}
            type={String(message).toLowerCase().includes("fail") || String(message).toLowerCase().includes("error") ? "error" : "success"}
          />
        )}
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
                  {scoring.matches && scoring.matches.length > 0 ? (
                    <div style={{ display: "grid", gap: 16 }}>
                      {scoring.matches.slice(0, 5).map((match, idx) => (
                        <div
                          key={idx}
                          style={{
                            background: "#f9fafb",
                            padding: 16,
                            borderRadius: 8,
                            border: "1px solid #e5e7eb",
                          }}
                        >
                          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}>
                            <div style={{ flex: 1 }}>
                              <h4 style={{ margin: "0 0 4px 0" }}>{match.job_title}</h4>
                              <p style={{ margin: 0, color: "#6b7280", fontSize: 14 }}>
                                {match.job_description?.substring(0, 100)}...
                              </p>
                            </div>
                            <div style={{ textAlign: "right", marginLeft: 16 }}>
                              <p style={{ margin: 0, fontSize: 24, fontWeight: 600, color: "#667eea" }}>
                                {formatPercent(match.score)}%
                              </p>
                              <p style={{ margin: 0, fontSize: 12, color: "#6b7280" }}>Match Score</p>
                            </div>
                          </div>
                          
                          {match.matched_skills && match.matched_skills.length > 0 && (
                            <div style={{ marginTop: 12 }}>
                              <p style={{ margin: "0 0 8px 0", fontSize: 12, fontWeight: 600, color: "#374151" }}>
                                Matched Skills:
                              </p>
                              <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                                {match.matched_skills.map((skill, i) => (
                                  <span
                                    key={i}
                                    style={{
                                      background: "#dbeafe",
                                      color: "#0369a1",
                                      padding: "4px 8px",
                                      borderRadius: 4,
                                      fontSize: 12,
                                    }}
                                  >
                                    {skill}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}
                          
                          {match.explanation && (
                            <div style={{ marginTop: 12 }}>
                              <p style={{ margin: 0, fontSize: 12, color: "#374151 " }}>
                                <strong>Summary:</strong> {match.explanation.summary || "Good skill match"}
                              </p>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p style={{ color: "#6b7280" }}>No matches found. Try adjusting your resume.</p>
                  )}
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
            {loadingHistory ? (
              <div style={{ textAlign: "center", padding: "40px 0" }}>
                <p>Loading history...</p>
              </div>
            ) : history && history.length > 0 ? (
              <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                {history.map((search, idx) => (
                  <div
                    key={idx}
                    style={{
                      background: "#fff",
                      padding: 24,
                      borderRadius: 12,
                      boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                      borderLeft: "4px solid #667eea",
                    }}
                  >
                    {/* Search Header Info */}
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "start",
                        marginBottom: 16,
                        paddingBottom: 12,
                        borderBottom: "1px solid #e5e7eb",
                      }}
                    >
                      <div>
                        <p style={{ margin: 0, fontWeight: 600, fontSize: 14, color: "#6b7280" }}>
                          Search ID: {search.search_id}
                        </p>
                        <p style={{ margin: "4px 0 0 0", fontSize: 13, color: "#9ca3af" }}>
                          Resume: {search.resume_path ? search.resume_path.split(/[\\/]/).pop() : "Unknown"}
                        </p>
                      </div>
                      <div style={{ textAlign: "right" }}>
                        <p style={{ margin: 0, fontSize: 12, color: "#9ca3af" }}>
                          {search.created_at
                            ? new Date(search.created_at).toLocaleDateString() +
                              " " +
                              new Date(search.created_at).toLocaleTimeString()
                            : "Date unknown"}
                        </p>
                        <button
                          onClick={() => deleteHistory(search.search_id)}
                          style={{
                            marginTop: 8,
                            padding: "6px 10px",
                            background: "#fff",
                            border: "1px solid #ef4444",
                            color: "#ef4444",
                            borderRadius: 6,
                            cursor: "pointer",
                            fontSize: 12,
                            fontWeight: 600,
                          }}
                        >
                          Delete
                        </button>
                      </div>
                    </div>

                    {/* Match Results */}
                    <div>
                      <p
                        style={{
                          margin: "0 0 12px 0",
                          fontWeight: 600,
                          fontSize: 14,
                          color: "#1f2937",
                        }}
                      >
                        Matched Jobs ({search.results ? search.results.length : 0})
                      </p>
                      {search.results && search.results.length > 0 ? (
                        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                          {search.results.map((result, resultIdx) => (
                            <div
                              key={resultIdx}
                              style={{
                                padding: 12,
                                background: "#f9fafb",
                                borderRadius: 8,
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                border: "1px solid #e5e7eb",
                              }}
                            >
                              <div>
                                <p style={{ margin: "0 0 4px 0", fontWeight: 600, fontSize: 14 }}>
                                  {result.job_title}
                                </p>
                                {result.matched_skills && result.matched_skills.length > 0 && (
                                  <p
                                    style={{
                                      margin: 0,
                                      fontSize: 12,
                                      color: "#6b7280",
                                    }}
                                  >
                                    Skills: {result.matched_skills.join(", ")}
                                  </p>
                                )}
                              </div>
                              <div
                                style={{
                                  display: "flex",
                                  alignItems: "center",
                                  gap: 8,
                                  marginLeft: 12,
                                }}
                              >
                                <div style={{ textAlign: "right" }}>
                                  <p
                                    style={{
                                      margin: 0,
                                      fontWeight: 700,
                                      fontSize: 18,
                                      color: "#667eea",
                                    }}
                                  >
                                    {formatPercent(result.score)}%
                                  </p>
                                  <p style={{ margin: "2px 0 0 0", fontSize: 11, color: "#9ca3af" }}>
                                    match
                                  </p>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p style={{ margin: 0, fontSize: 13, color: "#6b7280" }}>
                          No matches found for this resume.
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
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
            )}
          </div>
        )}
      </main>
    </div>
  );
}
