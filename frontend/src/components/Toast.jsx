import React from "react";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";

export default function Toast({ message, type = "info", onClose, duration = 4000 }) {
  const open = Boolean(message);

  const severity = type === "error" || String(message).toLowerCase().includes("fail") || String(message).toLowerCase().includes("error") ? "error" : "success";

  return (
    <Snackbar open={open} autoHideDuration={duration} onClose={onClose} anchorOrigin={{ vertical: "top", horizontal: "right" }}>
      <Alert onClose={onClose} severity={severity} sx={{ width: "100%" }}>
        {message}
      </Alert>
    </Snackbar>
  );
}
