import React, { useState } from "react";
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
      console.error("Login error:", err);
      const serverMsg = err?.response?.data?.detail || err?.response?.data || err?.response?.statusText;
      setMessage(serverMsg || err.message || "Login failed");
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
      console.error("Registration error:", err);
      const serverMsg = err?.response?.data?.detail || err?.response?.data || err?.response?.statusText;
      setMessage(serverMsg || err.message || "Registration failed");
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
