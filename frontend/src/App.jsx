import React, { useState, useEffect } from "react";
import axios from "axios";
import LoginPage from "./LoginPage";
import Dashboard from "./Dashboard";
import RecruiterDashboard from "./RecruiterDashboard";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

const theme = createTheme({
  palette: {
    primary: { main: "#3b82f6" },
    secondary: { main: "#6b7280" },
    background: { default: "#f4f6fb" },
  },
  typography: {
    fontFamily: 'Inter, Roboto, Arial, sans-serif',
  },
});

export default function App() {
  const [user, setUser] = useState(null);
  const API = "http://localhost:8000/api";
  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    delete axios.defaults.headers.common["Authorization"];
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");
    if (token && storedUser) {
      axios.defaults.headers.common["Authorization"] = "Bearer " + token;
      setUser(JSON.parse(storedUser));
    }

    // Response interceptor: if backend returns 401/403, force logout and redirect to login
    const id = axios.interceptors.response.use(
      (resp) => resp,
      (error) => {
        const status = error?.response?.status;
        if (status === 401 || status === 403) {
          try {
            // clear auth and reload to login
            handleLogout();
            window.location.reload();
          } catch (e) {}
        }
        return Promise.reject(error);
      }
    );

    return () => {
      axios.interceptors.response.eject(id);
    };
  }, []);

  if (!user) {
    return <LoginPage onLoginSuccess={setUser} />;
  }

  // Route to appropriate dashboard based on user role
  if (user.role === "recruiter") {
    return <RecruiterDashboard API={API} user={user} onLogout={handleLogout} />;
  }

  return <Dashboard user={user} onLogout={handleLogout} />;
}
