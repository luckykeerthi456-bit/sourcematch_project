#!/usr/bin/env python3
"""
Helper script to create React frontend files to bypass editor tool issues
"""
import os
from pathlib import Path

frontend_src = Path("c:/Users/2025/Desktop/sourcematch_project/frontend/src")

# Create LoginPage.jsx
login_page = """import React, { useState } from "react";
import axios from "axios";

const API = "http://localhost:8000/api";

export default function LoginPage({ onLoginSuccess }) {
  const [tab, setTab] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [role, setRole] = useState("candidate");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    try {
      const res = await axios.post(API + "/users/login", { email, password });
      const token = res.data.access_token;
      axios.defaults.headers.common["Authorization"] = "Bearer " + token;
      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(res.data.user));
      onLoginSuccess(res.data.user);
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    if (password !== confirmPassword) {
      setMessage("Passwords do not match");
      setLoading(false);
      return;
    }
    if (password.length < 6) {
      setMessage("Password must be at least 6 characters");
      setLoading(false);
      return;
    }
    try {
      await axios.post(API + "/users/register", {
        email,
        password,
        role,
        full_name: fullName,
      });
      const loginRes = await axios.post(API + "/users/login", { email, password });
      const token = loginRes.data.access_token;
      axios.defaults.headers.common["Authorization"] = "Bearer " + token;
      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(loginRes.data.user));
      onLoginSuccess(loginRes.data.user);
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div style={{ width: "100%", maxWidth: 420, padding: 20 }}>
        <div
          style={{
            background: "#fff",
            borderRadius: 16,
            padding: 40,
            boxShadow: "0 20px 60px rgba(0,0,0,0.3)",
          }}
        >
          <h1 style={{ textAlign: "center", color: "#667eea", margin: "0 0 8px 0" }}>
            SourceMatch
          </h1>
          <p style={{ textAlign: "center", color: "#6b7280", margin: 0 }}>
            Explainable AI for Recruitment
          </p>
          <div style={{ display: "flex", marginTop: 32, marginBottom: 24 }}>
            <button
              onClick={() => setTab("login")}
              style={{
                flex: 1,
                padding: "12px",
                border: "none",
                background: "none",
                fontSize: 16,
                fontWeight: tab === "login" ? "600" : "400",
                color: tab === "login" ? "#667eea" : "#6b7280",
                borderBottom: tab === "login" ? "3px solid #667eea" : "none",
                cursor: "pointer",
              }}
            >
              Login
            </button>
            <button
              onClick={() => setTab("register")}
              style={{
                flex: 1,
                padding: "12px",
                border: "none",
                background: "none",
                fontSize: 16,
                fontWeight: tab === "register" ? "600" : "400",
                color: tab === "register" ? "#667eea" : "#6b7280",
                borderBottom: tab === "register" ? "3px solid #667eea" : "none",
                cursor: "pointer",
              }}
            >
              Register
            </button>
          </div>

          {tab === "login" && (
            <form onSubmit={handleLogin}>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
                required
                style={{
                  width: "100%",
                  marginBottom: 12,
                  padding: "10px 12px",
                  border: "1px solid #d1d5db",
                  borderRadius: 8,
                  boxSizing: "border-box",
                }}
              />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                required
                style={{
                  width: "100%",
                  marginBottom: 24,
                  padding: "10px 12px",
                  border: "1px solid #d1d5db",
                  borderRadius: 8,
                  boxSizing: "border-box",
                }}
              />
              {message && (
                <div
                  style={{
                    padding: 12,
                    marginBottom: 16,
                    background: "#fee2e2",
                    color: "#991b1b",
                    borderRadius: 8,
                    fontSize: 14,
                  }}
                >
                  {message}
                </div>
              )}
              <button
                type="submit"
                disabled={loading}
                style={{
                  width: "100%",
                  padding: "12px",
                  background: "#667eea",
                  color: "#fff",
                  border: "none",
                  borderRadius: 8,
                  fontSize: 16,
                  fontWeight: 600,
                  cursor: "pointer",
                }}
              >
                {loading ? "Logging in..." : "Login"}
              </button>
              <p style={{ marginTop: 16, textAlign: "center", color: "#6b7280", fontSize: 14 }}>
                Don't have an account?{" "}
                <button
                  type="button"
                  onClick={() => setTab("register")}
                  style={{
                    border: "none",
                    background: "none",
                    color: "#667eea",
                    cursor: "pointer",
                    textDecoration: "underline",
                  }}
                >
                  Register
                </button>
              </p>
            </form>
          )}

          {tab === "register" && (
            <form onSubmit={handleRegister}>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Full Name"
                required
                style={{
                  width: "100%",
                  marginBottom: 12,
                  padding: "10px 12px",
                  border: "1px solid #d1d5db",
                  borderRadius: 8,
                  boxSizing: "border-box",
                }}
              />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
                required
                style={{
                  width: "100%",
                  marginBottom: 12,
                  padding: "10px 12px",
                  border: "1px solid #d1d5db",
                  borderRadius: 8,
                  boxSizing: "border-box",
                }}
              />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                required
                style={{
                  width: "100%",
                  marginBottom: 12,
                  padding: "10px 12px",
                  border: "1px solid #d1d5db",
                  borderRadius: 8,
                  boxSizing: "border-box",
                }}
              />
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm Password"
                required
                style={{
                  width: "100%",
                  marginBottom: 12,
                  padding: "10px 12px",
                  border: "1px solid #d1d5db",
                  borderRadius: 8,
                  boxSizing: "border-box",
                }}
              />
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                style={{
                  width: "100%",
                  marginBottom: 24,
                  padding: "10px 12px",
                  border: "1px solid #d1d5db",
                  borderRadius: 8,
                  boxSizing: "border-box",
                }}
              >
                <option value="candidate">Candidate (Job Seeker)</option>
                <option value="recruiter">Recruiter (Hiring Manager)</option>
              </select>
              {message && (
                <div
                  style={{
                    padding: 12,
                    marginBottom: 16,
                    background: "#fee2e2",
                    color: "#991b1b",
                    borderRadius: 8,
                    fontSize: 14,
                  }}
                >
                  {message}
                </div>
              )}
              <button
                type="submit"
                disabled={loading}
                style={{
                  width: "100%",
                  padding: "12px",
                  background: "#667eea",
                  color: "#fff",
                  border: "none",
                  borderRadius: 8,
                  fontSize: 16,
                  fontWeight: 600,
                  cursor: "pointer",
                }}
              >
                {loading ? "Creating..." : "Register"}
              </button>
              <p style={{ marginTop: 16, textAlign: "center", color: "#6b7280", fontSize: 14 }}>
                Already have an account?{" "}
                <button
                  type="button"
                  onClick={() => setTab("login")}
                  style={{
                    border: "none",
                    background: "none",
                    color: "#667eea",
                    cursor: "pointer",
                    textDecoration: "underline",
                  }}
                >
                  Login
                </button>
              </p>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
"""

# Create Dashboard.jsx
dashboard = """import React from "react";

export default function Dashboard({ user, onLogout }) {
  return (
    <div style={{ fontFamily: "Arial, sans-serif", background: "#F8FAFF", minHeight: "100vh" }}>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: 20,
          background: "#6C5CE7",
          color: "#fff",
        }}
      >
        <h1 style={{ margin: 0 }}>SourceMatch</h1>
        <div>
          <span style={{ marginRight: 12 }}>
            {user.full_name} ({user.role})
          </span>
          <button
            onClick={onLogout}
            style={{
              background: "#fff",
              color: "#6C5CE7",
              border: "none",
              padding: "8px 12px",
              borderRadius: 8,
              cursor: "pointer",
            }}
          >
            Logout
          </button>
        </div>
      </header>
      <main style={{ maxWidth: 1200, margin: "24px auto", padding: 20 }}>
        <h2>Welcome, {user.full_name}!</h2>
        <div
          style={{
            background: "#fff",
            padding: 20,
            borderRadius: 12,
            boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
          }}
        >
          <p>
            <strong>Email:</strong> {user.email}
          </p>
          <p>
            <strong>Role:</strong> {user.role === "candidate" ? "Job Seeker" : "Recruiter"}
          </p>
          <p style={{ color: "#059669" }}>
            You are now successfully logged in with secure database authentication!
          </p>
        </div>
      </main>
    </div>
  );
}
"""

# Create App.jsx
app = """import React, { useState, useEffect } from "react";
import axios from "axios";
import LoginPage from "./LoginPage";
import Dashboard from "./Dashboard";

export default function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");
    if (token && storedUser) {
      axios.defaults.headers.common["Authorization"] = "Bearer " + token;
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    delete axios.defaults.headers.common["Authorization"];
  };

  if (!user) {
    return <LoginPage onLoginSuccess={setUser} />;
  }

  return <Dashboard user={user} onLogout={handleLogout} />;
}
"""

# Create index.js
index_js = """import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""

# Create index.css
index_css = """* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
"""

# Write all files
os.makedirs(frontend_src, exist_ok=True)

with open(frontend_src / "LoginPage.jsx", "w", encoding="utf-8") as f:
    f.write(login_page)
print("✓ Created LoginPage.jsx")

with open(frontend_src / "Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(dashboard)
print("✓ Created Dashboard.jsx")

with open(frontend_src / "App.jsx", "w", encoding="utf-8") as f:
    f.write(app)
print("✓ Created App.jsx")

with open(frontend_src / "index.js", "w", encoding="utf-8") as f:
    f.write(index_js)
print("✓ Created index.js")

with open(frontend_src / "index.css", "w", encoding="utf-8") as f:
    f.write(index_css)
print("✓ Created index.css")

print("\\nAll React files created successfully!")
