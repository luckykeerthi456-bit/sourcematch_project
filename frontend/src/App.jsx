import React, { useState, useEffect } from "react";
import axios from "axios";
import LoginPage from "./LoginPage";
import Dashboard from "./Dashboard";
import RecruiterDashboard from "./RecruiterDashboard";

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

  // Route to appropriate dashboard based on user role
  if (user.role === "recruiter") {
    return <RecruiterDashboard user={user} onLogout={handleLogout} />;
  }

  return <Dashboard user={user} onLogout={handleLogout} />;
}
