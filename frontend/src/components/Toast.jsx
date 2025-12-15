import React, { useEffect } from "react";

export default function Toast({ message, type = "info", onClose, duration = 4000 }) {
  useEffect(() => {
    if (!message) return;
    const t = setTimeout(() => {
      onClose && onClose();
    }, duration);
    return () => clearTimeout(t);
  }, [message, duration, onClose]);

  if (!message) return null;

  const isError = type === "error" || String(message).toLowerCase().includes("fail") || String(message).toLowerCase().includes("error");
  const bg = isError ? "#FEF2F2" : "#ECFDF5"; // light red / light green
  const border = isError ? "#FCA5A5" : "#86EFAC";
  const color = isError ? "#991B1B" : "#064E3B";

  const containerStyle = {
    position: "fixed",
    right: 20,
    top: 20,
    zIndex: 9999,
    minWidth: 280,
    maxWidth: "80%",
    background: bg,
    border: `1px solid ${border}`,
    color,
    padding: "12px 16px",
    borderRadius: 8,
    boxShadow: "0 6px 18px rgba(0,0,0,0.08)",
    fontSize: 14,
  };

  const closeBtn = {
    marginLeft: 12,
    background: "transparent",
    border: "none",
    color,
    cursor: "pointer",
    fontWeight: 700,
  };

  return (
    <div style={containerStyle} role="status" aria-live="polite">
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ flex: 1, marginRight: 8 }}>{message}</div>
        <button aria-label="Close" onClick={() => onClose && onClose()} style={closeBtn}>
          ✕
        </button>
      </div>
    </div>
  );
}
