import React, { useState, useEffect } from "react";
import axios from "axios";
import Toast from "./components/Toast";
import ConfirmModal from "./components/ConfirmModal";
export default function RecruiterDashboard({ API, user, onLogout }) {
  const [activeTab, setActiveTab] = useState("applications");
  const [applications, setApplications] = useState([]);
  const [users, setUsers] = useState([]);
  const [selectedApp, setSelectedApp] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [confirmMessage, setConfirmMessage] = useState("");
  const [confirmAction, setConfirmAction] = useState(() => () => {});
  const [filterStatus, setFilterStatus] = useState("all");
  // Job posting form state for recruiters
  const [jobTitle, setJobTitle] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [company, setCompany] = useState("");
  const [location, setLocation] = useState("");
  const [salaryMin, setSalaryMin] = useState("");
  const [salaryMax, setSalaryMax] = useState("");
  const [experienceLevel, setExperienceLevel] = useState("Mid-level");
  const [requiredSkills, setRequiredSkills] = useState("");

  // Helper to format scores robustly to 0-100 percent
  const formatPercent = (score) => {
    const s = Number(score) || 0;
    let perc = 0;
    if (s <= 1) {
      perc = s * 100;
    } else if (s > 1 && s <= 10) {
      perc = s * 10;
    } else if (s > 10 && s <= 100) {
      perc = s;
    } else {
      perc = s;
    }
    perc = Math.max(0, Math.min(100, perc));
    return Math.round(perc);
  };

  // Load applications when tab changes
  useEffect(() => {
    if (activeTab === "applications") {
      fetchApplications();
    } else if (activeTab === "users") {
      fetchUsers();
    }
  }, [activeTab, filterStatus]);

  const fetchApplications = async () => {
    setLoading(true);
    try {
      let url = API + "/applications/recruiter/applications";
      if (filterStatus !== "all") {
        url += `?status=${filterStatus}`;
      }
      const res = await axios.get(url);
      setApplications(res.data || []);
    } catch (err) {
      console.error("Failed to load applications:", err);
      setMessage("Failed to load applications");
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await axios.get(API + "/users/recruiter/users");
      setUsers(res.data || []);
    } catch (err) {
      console.error("Failed to load users:", err);
      setMessage("Failed to load users");
    } finally {
      setLoading(false);
    }
  };

  const fetchApplicationDetails = async (applicationId) => {
    try {
      const res = await axios.get(
        API + `/applications/recruiter/applications/${applicationId}`
      );
      setSelectedApp(res.data);
    } catch (err) {
      console.error("Failed to load application details:", err);
      setMessage("Failed to load application details");
    }
  };

  const updateApplicationStatus = async (applicationId, newStatus) => {
    try {
      const formData = new FormData();
      formData.append("status", newStatus);
      
      console.log("Sending update request to:", API + `/applications/recruiter/applications/${applicationId}/status`);
      console.log("Status:", newStatus);
      
      // Let the browser/axios set the Content-Type including boundary for multipart data.
      const response = await axios.put(
        API + `/applications/recruiter/applications/${applicationId}/status`,
        formData
      );
      
      console.log("Response:", response.data);
      setMessage(`Application ${newStatus} successfully!`);
      setSelectedApp(null);
      await fetchApplications();
    } catch (err) {
      console.error("Failed to update status:", err);
      console.error("Error details:", err.response?.data);
      setMessage(err?.response?.data?.detail || "Failed to update status");
    }
  };

  const deleteApplication = async (applicationId) => {
    // open confirm modal and perform deletion if confirmed
    setConfirmMessage("Are you sure you want to delete this application? This cannot be undone.");
    setConfirmAction(() => async () => {
      try {
        await axios.delete(API + `/applications/recruiter/applications/${applicationId}`);
        setMessage("Application deleted");
        setSelectedApp(null);
        await fetchApplications();
      } catch (err) {
        console.error("Failed to delete application:", err);
        setMessage(err?.response?.data?.detail || "Failed to delete application");
      }
      setConfirmOpen(false);
    });
    setConfirmOpen(true);
  };

  const downloadResume = (resumePath) => {
    if (resumePath) {
      const link = document.createElement("a");
      link.href = `/resumes/${resumePath.split("/").pop()}`;
      link.download = resumePath.split("/").pop();
      link.click();
    }
  };

  const deleteUser = async (userId) => {
    setConfirmMessage("Are you sure you want to permanently delete this user and all their data? This action cannot be undone.");
    setConfirmAction(() => async () => {
      try {
        await axios.delete(API + `/users/recruiter/users/${userId}`);
        setMessage("User deleted");
        await fetchUsers();
      } catch (err) {
        console.error("Failed to delete user:", err);
        setMessage(err?.response?.data?.detail || "Failed to delete user");
      }
      setConfirmOpen(false);
    });
    setConfirmOpen(true);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "shortlisted":
        return "#10b981";
      case "rejected":
        return "#ef4444";
      default:
        return "#6b7280";
    }
  };

  const getStatusBgColor = (status) => {
    switch (status) {
      case "shortlisted":
        return "#d1fae5";
      case "rejected":
        return "#fee2e2";
      default:
        return "#f3f4f6";
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
          <h1 style={{ margin: "0 0 4px 0" }}>SourceMatch - Recruiter Portal</h1>
          <p style={{ margin: 0, fontSize: 12, opacity: 0.9 }}>Manage Applications & Review Candidates</p>
        </div>
        <div style={{ textAlign: "right" }}>
          <p style={{ margin: "0 0 8px 0", fontSize: 14 }}>
            {user.full_name} • 👔 Recruiter
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
          { id: "applications", label: "📋 Applications", show: true },
          { id: "post_job", label: "➕ Post Job", show: true },
          { id: "users", label: "� Users", show: true },
          { id: "stats", label: "�📊 Statistics", show: true },
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
      <main style={{ maxWidth: 1400, margin: "0 auto", padding: "24px" }}>
        {message && (
          <Toast
            message={message}
            onClose={() => setMessage("")}
            type={String(message).toLowerCase().includes("fail") || String(message).toLowerCase().includes("error") ? "error" : "success"}
          />
        )}
        <ConfirmModal
          open={confirmOpen}
          title={"Please confirm"}
          message={confirmMessage}
          onConfirm={() => {
            try {
              confirmAction();
            } catch (e) {
              // if confirmAction is async, it already runs; swallow errors here
            }
          }}
          onCancel={() => setConfirmOpen(false)}
        />

        {/* APPLICATIONS TAB */}
        {activeTab === "applications" && (
          <div>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: 24,
              }}
            >
              <h2>Applications</h2>
              <div style={{ display: "flex", gap: 8 }}>
                {["all", "applied", "shortlisted", "rejected"].map((status) => (
                  <button
                    key={status}
                    onClick={() => setFilterStatus(status)}
                    style={{
                      padding: "8px 16px",
                      background: filterStatus === status ? "#667eea" : "#e5e7eb",
                      color: filterStatus === status ? "#fff" : "#374151",
                      border: "none",
                      borderRadius: 6,
                      cursor: "pointer",
                      fontWeight: 600,
                      fontSize: 12,
                    }}
                  >
                    {status.charAt(0).toUpperCase() + status.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            {loading ? (
              <p>Loading applications...</p>
            ) : selectedApp ? (
              // Detailed Application View
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: 24,
                }}
              >
                {/* Left Side: Candidate Info */}
                <div
                  style={{
                    background: "#fff",
                    padding: 24,
                    borderRadius: 12,
                    boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                  }}
                >
                  <button
                    onClick={() => setSelectedApp(null)}
                    style={{
                      background: "transparent",
                      border: "none",
                      color: "#667eea",
                      cursor: "pointer",
                      fontWeight: 600,
                      marginBottom: 16,
                      fontSize: 14,
                    }}
                  >
                    ← Back to List
                  </button>

                  <h3 style={{ margin: "0 0 16px 0" }}>Candidate Profile</h3>

                  <div style={{ borderBottom: "1px solid #e5e7eb", paddingBottom: 16, marginBottom: 16 }}>
                    <p style={{ margin: "0 0 8px 0", color: "#6b7280", fontSize: 12 }}>
                      Full Name
                    </p>
                    <p style={{ margin: "0 0 12px 0", fontSize: 16, fontWeight: 600 }}>
                      {selectedApp.candidate_name}
                    </p>

                    <p style={{ margin: "0 0 8px 0", color: "#6b7280", fontSize: 12 }}>
                      Email
                    </p>
                    <p
                      style={{
                        margin: "0 0 12px 0",
                        fontSize: 14,
                        color: "#667eea",
                        wordBreak: "break-all",
                      }}
                    >
                      <a
                        href={`mailto:${selectedApp.candidate_email}`}
                        style={{ color: "#667eea", textDecoration: "none" }}
                      >
                        {selectedApp.candidate_email}
                      </a>
                    </p>
                  </div>

                  <div style={{ borderBottom: "1px solid #e5e7eb", paddingBottom: 16, marginBottom: 16 }}>
                    <p style={{ margin: "0 0 8px 0", color: "#6b7280", fontSize: 12 }}>
                      Applied for
                    </p>
                    <p style={{ margin: "0 0 12px 0", fontSize: 16, fontWeight: 600 }}>
                      {selectedApp.job_title}
                    </p>
                  </div>

                  {/* Additional profile fields extracted from resume */}
                  <div style={{ borderBottom: "1px solid #e5e7eb", paddingBottom: 16, marginBottom: 16 }}>
                    <p style={{ margin: "0 0 8px 0", color: "#6b7280", fontSize: 12 }}>
                      Profile
                    </p>
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
                      <div>
                        <p style={{ margin: "0 0 4px 0", fontSize: 14 }}><strong>Date of Birth</strong></p>
                        <p style={{ margin: 0, color: "#374151", fontSize: 14 }}>{selectedApp.date_of_birth || "—"}</p>
                      </div>

                      <div>
                        <p style={{ margin: "0 0 4px 0", fontSize: 14 }}><strong>Course</strong></p>
                        <p style={{ margin: 0, color: "#374151", fontSize: 14 }}>{selectedApp.course || "—"}</p>
                      </div>

                      <div>
                        <p style={{ margin: "12px 0 4px 0", fontSize: 14 }}><strong>Year of Passing</strong></p>
                        <p style={{ margin: 0, color: "#374151", fontSize: 14 }}>{selectedApp.year_of_passing || "—"}</p>
                      </div>

                      <div>
                        <p style={{ margin: "12px 0 4px 0", fontSize: 14 }}><strong>Skills</strong></p>
                        {selectedApp.candidate_skills && selectedApp.candidate_skills.length > 0 ? (
                          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                            {selectedApp.candidate_skills.map((s, i) => (
                              <span key={i} style={{ background: "#eef2ff", color: "#3730a3", padding: "4px 8px", borderRadius: 4, fontSize: 12, fontWeight: 500 }}>{s}</span>
                            ))}
                          </div>
                        ) : (
                          <p style={{ margin: 0, color: "#6b7280" }}>No profile skills found</p>
                        )}
                      </div>
                    </div>
                  </div>

                  <div style={{ borderBottom: "1px solid #e5e7eb", paddingBottom: 16, marginBottom: 16 }}>
                    <p style={{ margin: "0 0 8px 0", color: "#6b7280", fontSize: 12 }}>
                      Match Score
                    </p>
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 12,
                        marginBottom: 12,
                      }}
                    >
                      <div
                        style={{
                          width: "100%",
                          background: "#e5e7eb",
                          height: 8,
                          borderRadius: 4,
                          overflow: "hidden",
                        }}
                      >
                        <div
                          style={{
                            width: `${formatPercent(selectedApp.score)}%`,
                            background: "#667eea",
                            height: "100%",
                          }}
                        />
                      </div>
                      <p
                        style={{
                          margin: 0,
                          fontWeight: 700,
                          fontSize: 16,
                          color: "#667eea",
                          minWidth: 50,
                        }}
                      >
                        {formatPercent(selectedApp.score)}%
                      </p>
                    </div>
                  </div>

                  <div style={{ marginBottom: 16 }}>
                    <p style={{ margin: "0 0 8px 0", color: "#6b7280", fontSize: 12 }}>
                      Matched Skills
                    </p>
                    {selectedApp.explanation?.matched_skills &&
                    selectedApp.explanation.matched_skills.length > 0 ? (
                      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                        {selectedApp.explanation.matched_skills.map((skill, idx) => (
                          <span
                            key={idx}
                            style={{
                              background: "#d1fae5",
                              color: "#065f46",
                              padding: "4px 8px",
                              borderRadius: 4,
                              fontSize: 12,
                              fontWeight: 500,
                            }}
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <p style={{ margin: 0, color: "#6b7280" }}>No matched skills</p>
                    )}
                  </div>

                  <p style={{ margin: "0 0 8px 0", color: "#6b7280", fontSize: 12 }}>
                    Application Date
                  </p>
                  <p style={{ margin: 0, fontSize: 14 }}>
                    {selectedApp.created_at
                      ? new Date(selectedApp.created_at).toLocaleDateString() +
                        " " +
                        new Date(selectedApp.created_at).toLocaleTimeString()
                      : "Unknown"}
                  </p>
                </div>

                {/* Right Side: Resume & Actions */}
                <div
                  style={{
                    background: "#fff",
                    padding: 24,
                    borderRadius: 12,
                    boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                    display: "flex",
                    flexDirection: "column",
                  }}
                >
                  <h3 style={{ margin: "0 0 16px 0" }}>Resume & Actions</h3>

                  {/* Resume Preview */}
                  <div
                    style={{
                      background: "#f9fafb",
                      padding: 16,
                      borderRadius: 8,
                      marginBottom: 16,
                      border: "1px solid #e5e7eb",
                      maxHeight: 400,
                      overflow: "auto",
                      flex: 1,
                    }}
                  >
                    <p style={{ margin: "0 0 12px 0", fontWeight: 600, color: "#6b7280" }}>
                      Resume Preview:
                    </p>
                    <p
                      style={{
                        margin: 0,
                        color: "#374151",
                        lineHeight: 1.6,
                        whiteSpace: "pre-wrap",
                        wordWrap: "break-word",
                        fontSize: 13,
                      }}
                    >
                      {selectedApp.resume_text || "No resume text available"}
                    </p>
                  </div>

                  {/* Action Buttons */}
                  <div style={{ display: "flex", gap: 12, flexDirection: "column" }}>
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
                      <button
                        onClick={() => updateApplicationStatus(selectedApp.application_id, "shortlisted")}
                        style={{
                          padding: "12px 16px",
                          background: "#10b981",
                          color: "#fff",
                          border: "none",
                          borderRadius: 6,
                          cursor: "pointer",
                          fontWeight: 600,
                          fontSize: 14,
                        }}
                      >
                        ✓ Shortlist
                      </button>

                      <button
                        onClick={() => updateApplicationStatus(selectedApp.application_id, "rejected")}
                        style={{
                          padding: "12px 16px",
                          background: "#ef4444",
                          color: "#fff",
                          border: "none",
                          borderRadius: 6,
                          cursor: "pointer",
                          fontWeight: 600,
                          fontSize: 14,
                        }}
                      >
                        ✗ Reject
                      </button>
                    </div>

                    <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
                      <button
                        onClick={() => deleteApplication(selectedApp.application_id)}
                        style={{
                          padding: "12px 16px",
                          background: "#ef4444",
                          color: "#fff",
                          border: "none",
                          borderRadius: 6,
                          cursor: "pointer",
                          fontWeight: 600,
                          fontSize: 14,
                        }}
                      >
                        🗑 Delete Application
                      </button>
                    </div>

                    <a
                      href={`mailto:${selectedApp.candidate_email}`}
                      style={{
                        padding: "12px 16px",
                        background: "#667eea",
                        color: "#fff",
                        border: "none",
                        borderRadius: 6,
                        cursor: "pointer",
                        fontWeight: 600,
                        fontSize: 14,
                        textDecoration: "none",
                        textAlign: "center",
                      }}
                    >
                      📧 Send Email
                    </a>
                  </div>

                  <div
                    style={{
                      marginTop: 16,
                      padding: 12,
                      background: "#f0fdf4",
                      borderRadius: 6,
                      borderLeft: "4px solid #10b981",
                    }}
                  >
                    <p style={{ margin: 0, fontSize: 12, color: "#166534" }}>
                      Current Status:{" "}
                      <span
                        style={{
                          fontWeight: 600,
                          color: getStatusColor(selectedApp.status),
                        }}
                      >
                        {selectedApp.status.toUpperCase()}
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              // Applications List View
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                {applications && applications.length > 0 ? (
                  applications.map((app) => (
                    <div
                      key={app.application_id}
                      style={{
                        background: "#fff",
                        padding: 16,
                        borderRadius: 12,
                        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        cursor: "pointer",
                        transition: "all 0.3s",
                        border: "2px solid transparent",
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.borderColor = "#667eea";
                        e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.12)";
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.borderColor = "transparent";
                        e.currentTarget.style.boxShadow = "0 2px 8px rgba(0,0,0,0.08)";
                      }}
                      onClick={() => fetchApplicationDetails(app.application_id)}
                    >
                      <div style={{ flex: 1 }}>
                        <p style={{ margin: "0 0 4px 0", fontWeight: 600, fontSize: 16 }}>
                          {app.candidate_name}
                        </p>
                        <p
                          style={{
                            margin: "0 0 8px 0",
                            color: "#6b7280",
                            fontSize: 14,
                          }}
                        >
                          Applied for: <strong>{app.job_title}</strong>
                        </p>
                        <p
                          style={{
                            margin: 0,
                            color: "#9ca3af",
                            fontSize: 12,
                          }}
                        >
                          {app.candidate_email}
                        </p>
                      </div>

                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: 24,
                          marginLeft: 16,
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
                            {formatPercent(app.score)}%
                          </p>
                          <p style={{ margin: "2px 0 0 0", fontSize: 12, color: "#6b7280" }}>
                            match
                          </p>
                        </div>

                        <div
                          style={{
                            padding: "6px 12px",
                            background: getStatusBgColor(app.status),
                            color: getStatusColor(app.status),
                            borderRadius: 20,
                            fontSize: 12,
                            fontWeight: 600,
                            minWidth: 100,
                            textAlign: "center",
                          }}
                        >
                          {app.status.charAt(0).toUpperCase() + app.status.slice(1)}
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <div
                    style={{
                      background: "#fff",
                      padding: 40,
                      borderRadius: 12,
                      textAlign: "center",
                      color: "#6b7280",
                    }}
                  >
                    <p>No applications found</p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* USERS TAB */}
        {/* POST JOB TAB */}
        {activeTab === "post_job" && (
          <div>
            <h2>Post a New Job</h2>
            <div style={{ maxWidth: 800, background: "#fff", padding: 20, borderRadius: 8, boxShadow: "0 2px 8px rgba(0,0,0,0.06)" }}>
              <label style={{ display: "block", marginBottom: 8, fontWeight: 600 }}>Job Title</label>
              <input value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} style={{ width: "100%", padding: 8, marginBottom: 12 }} />

              <label style={{ display: "block", marginBottom: 8, fontWeight: 600 }}>Company</label>
              <input value={company} onChange={(e) => setCompany(e.target.value)} style={{ width: "100%", padding: 8, marginBottom: 12 }} />

              <label style={{ display: "block", marginBottom: 8, fontWeight: 600 }}>Location</label>
              <input value={location} onChange={(e) => setLocation(e.target.value)} style={{ width: "100%", padding: 8, marginBottom: 12 }} />

              <label style={{ display: "block", marginBottom: 8, fontWeight: 600 }}>Description</label>
              <textarea value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} rows={6} style={{ width: "100%", padding: 8, marginBottom: 12 }} />

              <label style={{ display: "block", marginBottom: 8, fontWeight: 600 }}>Required skills (comma separated)</label>
              <input value={requiredSkills} onChange={(e) => setRequiredSkills(e.target.value)} style={{ width: "100%", padding: 8, marginBottom: 12 }} />

              <div style={{ display: "flex", gap: 12 }}>
                <div style={{ flex: 1 }}>
                  <label style={{ display: "block", marginBottom: 8, fontWeight: 600 }}>Salary Min</label>
                  <input value={salaryMin} onChange={(e) => setSalaryMin(e.target.value)} type="number" style={{ width: "100%", padding: 8 }} />
                </div>
                <div style={{ flex: 1 }}>
                  <label style={{ display: "block", marginBottom: 8, fontWeight: 600 }}>Salary Max</label>
                  <input value={salaryMax} onChange={(e) => setSalaryMax(e.target.value)} type="number" style={{ width: "100%", padding: 8 }} />
                </div>
                <div style={{ flex: 1 }}>
                  <label style={{ display: "block", marginBottom: 8, fontWeight: 600 }}>Experience</label>
                  <select value={experienceLevel} onChange={(e) => setExperienceLevel(e.target.value)} style={{ width: "100%", padding: 8 }}>
                    <option>Entry-level</option>
                    <option>Mid-level</option>
                    <option>Senior</option>
                    <option>Lead</option>
                  </select>
                </div>
              </div>

              <div style={{ marginTop: 16, display: "flex", gap: 8 }}>
                <button
                  onClick={async () => {
                    // basic client-side validation
                    if (!jobTitle.trim() || !jobDescription.trim()) {
                      setMessage("Please provide a job title and description");
                      return;
                    }
                    try {
                      setLoading(true);
                      const payload = {
                        title: jobTitle,
                        description: jobDescription,
                        company: company || undefined,
                        location: location || undefined,
                        salary_min: salaryMin ? Number(salaryMin) : undefined,
                        salary_max: salaryMax ? Number(salaryMax) : undefined,
                        experience_level: experienceLevel,
                        required_skills: requiredSkills || undefined,
                      };
                      const res = await axios.post(API + "/jobs", payload);
                      setMessage("Job posted successfully");
                      // reset form
                      setJobTitle("");
                      setJobDescription("");
                      setCompany("");
                      setLocation("");
                      setSalaryMin("");
                      setSalaryMax("");
                      setRequiredSkills("");
                      setExperienceLevel("Mid-level");
                      // optionally go back to jobs list or applications
                      setActiveTab("stats");
                    } catch (err) {
                      console.error("Failed to post job:", err);
                      setMessage(err?.response?.data?.detail || "Failed to post job");
                    } finally {
                      setLoading(false);
                    }
                  }}
                  style={{ padding: "10px 16px", background: "#10b981", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer", fontWeight: 700 }}
                >
                  Publish Job
                </button>

                <button onClick={() => { setJobTitle(""); setJobDescription(""); setCompany(""); setLocation(""); setSalaryMin(""); setSalaryMax(""); setRequiredSkills(""); setExperienceLevel("Mid-level"); }} style={{ padding: "10px 16px", background: "#e5e7eb", border: "none", borderRadius: 6, cursor: "pointer" }}>
                  Reset
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === "users" && (
          <div>
            <h2>Users</h2>
            {loading ? (
              <p>Loading users...</p>
            ) : users && users.length > 0 ? (
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                {users.map((u) => (
                  <div
                    key={u.id}
                    style={{
                      background: "#fff",
                      padding: 16,
                      borderRadius: 12,
                      boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                    }}
                  >
                    <div>
                      <p style={{ margin: "0 0 4px 0", fontWeight: 600 }}>{u.full_name || '—'}</p>
                      <p style={{ margin: 0, color: "#6b7280", fontSize: 13 }}>{u.email}</p>
                      <p style={{ margin: 0, color: "#9ca3af", fontSize: 12 }}>{u.role}</p>
                    </div>
                    <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                      <p style={{ margin: 0, color: "#9ca3af", fontSize: 12 }}>
                        {u.created_at ? new Date(u.created_at).toLocaleString() : ''}
                      </p>
                      <button
                        onClick={() => deleteUser(u.id)}
                        style={{
                          padding: "8px 12px",
                          background: "#ef4444",
                          color: "#fff",
                          border: "none",
                          borderRadius: 6,
                          cursor: "pointer",
                          fontWeight: 600,
                        }}
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{ background: "#fff", padding: 24, borderRadius: 12, textAlign: "center", color: "#6b7280" }}>
                <p>No users found</p>
              </div>
            )}
          </div>
        )}

        {/* STATISTICS TAB */}
        {activeTab === "stats" && (
          <div>
            <h2>Statistics</h2>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
                gap: 20,
                marginTop: 20,
              }}
            >
              <div
                style={{
                  background: "#fff",
                  padding: 24,
                  borderRadius: 12,
                  boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                }}
              >
                <p style={{ margin: "0 0 8px 0", color: "#6b7280", fontSize: 14 }}>
                  Total Applications
                </p>
                <p style={{ margin: 0, fontSize: 32, fontWeight: 700, color: "#667eea" }}>
                  {applications.length}
                </p>
              </div>

              <div
                style={{
                  background: "#fff",
                  padding: 24,
                  borderRadius: 12,
                  boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                }}
              >
                <p style={{ margin: "0 0 8px 0", color: "#6b7280", fontSize: 14 }}>
                  Shortlisted
                </p>
                <p style={{ margin: 0, fontSize: 32, fontWeight: 700, color: "#10b981" }}>
                  {applications.filter((a) => a.status === "shortlisted").length}
                </p>
              </div>

              <div
                style={{
                  background: "#fff",
                  padding: 24,
                  borderRadius: 12,
                  boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                }}
              >
                <p style={{ margin: "0 0 8px 0", color: "#6b7280", fontSize: 14 }}>
                  Rejected
                </p>
                <p style={{ margin: 0, fontSize: 32, fontWeight: 700, color: "#ef4444" }}>
                  {applications.filter((a) => a.status === "rejected").length}
                </p>
              </div>

              <div
                style={{
                  background: "#fff",
                  padding: 24,
                  borderRadius: 12,
                  boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                }}
              >
                <p style={{ margin: "0 0 8px 0", color: "#6b7280", fontSize: 14 }}>
                  Pending Review
                </p>
                <p style={{ margin: 0, fontSize: 32, fontWeight: 700, color: "#f59e0b" }}>
                  {applications.filter((a) => a.status === "applied").length}
                </p>
              </div>
            </div>

            <div
              style={{
                background: "#fff",
                padding: 24,
                borderRadius: 12,
                boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                marginTop: 20,
              }}
            >
              <h3 style={{ margin: "0 0 20px 0" }}>Top Matches</h3>
              {applications.length > 0 ? (
                <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                  {applications
                    .sort((a, b) => (b.score || 0) - (a.score || 0))
                    .slice(0, 5)
                    .map((app, idx) => (
                      <div
                        key={idx}
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                          paddingBottom: 12,
                          borderBottom:
                            idx < 4 ? "1px solid #e5e7eb" : "none",
                        }}
                      >
                        <div>
                          <p style={{ margin: "0 0 4px 0", fontWeight: 600 }}>
                            {app.candidate_name}
                          </p>
                          <p style={{ margin: 0, color: "#6b7280", fontSize: 12 }}>
                            {app.job_title}
                          </p>
                        </div>
                        <p
                          style={{
                            margin: 0,
                            fontWeight: 700,
                            fontSize: 18,
                            color: "#667eea",
                          }}
                        >
                          {formatPercent(app.score)}%
                        </p>
                      </div>
                    ))}
                </div>
              ) : (
                <p style={{ color: "#6b7280" }}>No applications yet</p>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
