import React, { useState, useEffect } from "react";
import axios from "axios";
import Toast from "./components/Toast";
import ConfirmModal from "./components/ConfirmModal";
import { DataGrid } from "@mui/x-data-grid";
import { Button, CircularProgress, Box, Typography, Modal } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";

export default function RecruiterDashboard({ API, user, onLogout }) {
  const [activeTab, setActiveTab] = useState("applications");
  const [applications, setApplications] = useState([]);
  const [users, setUsers] = useState([]);
  const [jobs, setJobs] = useState([]);
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
    } else if (activeTab === "jobs") {
      fetchJobs();
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

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const res = await axios.get(API + "/jobs");
      setJobs(res.data || []);
    } catch (err) {
      console.error("Failed to load jobs:", err);
      setMessage("Failed to load jobs");
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

  const deleteJob = async (jobId) => {
    setConfirmMessage("Are you sure you want to delete this job? This cannot be undone.");
    setConfirmAction(() => async () => {
      try {
        await axios.delete(API + `/jobs/${jobId}`);
        setMessage("Job deleted");
        await fetchJobs();
      } catch (err) {
        console.error("Failed to delete job:", err);
        setMessage(err?.response?.data?.detail || "Failed to delete job");
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

  const renderJobsTab = () => (
    <Box>
      <Typography variant="h4" gutterBottom>
        Manage Jobs
      </Typography>
      {loading ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="200px">
          <CircularProgress />
        </Box>
      ) : (
        <DataGrid
          rows={jobs.map((job) => ({ id: job.id, ...job }))}
          columns={[
            { field: "title", headerName: "Title", flex: 1 },
            { field: "company", headerName: "Company", flex: 1 },
            { field: "location", headerName: "Location", flex: 1 },
            {
              field: "actions",
              headerName: "Actions",
              renderCell: (params) => (
                <Button
                  variant="contained"
                  color="error"
                  startIcon={<DeleteIcon />}
                  onClick={() => deleteJob(params.row.id)}
                >
                  Delete
                </Button>
              ),
              flex: 1,
            },
          ]}
          autoHeight
          pageSize={5}
          rowsPerPageOptions={[5, 10, 20]}
        />
      )}
    </Box>
  );

  return (
    <Box>
      <Box display="flex" justifyContent="space-around" mb={2}>
        <Button variant={activeTab === "applications" ? "contained" : "outlined"} onClick={() => setActiveTab("applications")}>
          Applications
        </Button>
        <Button variant={activeTab === "users" ? "contained" : "outlined"} onClick={() => setActiveTab("users")}>
          Users
        </Button>
        <Button variant={activeTab === "jobs" ? "contained" : "outlined"} onClick={() => setActiveTab("jobs")}>
          Manage Jobs
        </Button>
      </Box>
      {message && <Toast message={message} onClose={() => setMessage("")} />}
      <Modal open={confirmOpen} onClose={() => setConfirmOpen(false)}>
        <Box p={3} bgcolor="white" borderRadius={2} boxShadow={3} mx="auto" my="20%" width="300px">
          <Typography variant="h6" gutterBottom>
            {confirmMessage}
          </Typography>
          <Box display="flex" justifyContent="space-between">
            <Button variant="contained" color="primary" onClick={confirmAction}>
              Confirm
            </Button>
            <Button variant="outlined" onClick={() => setConfirmOpen(false)}>
              Cancel
            </Button>
          </Box>
        </Box>
      </Modal>
      {activeTab === "jobs" && renderJobsTab()}
    </Box>
  );
}
