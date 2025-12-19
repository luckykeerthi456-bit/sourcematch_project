import React from "react";

export default function ConfirmModal({ open, title = "Confirm", message, onConfirm, onCancel, confirmLabel = "Confirm", cancelLabel = "Cancel" }) {
  if (!open) return null;

  const overlay = {
    position: "fixed",
    left: 0,
    top: 0,
    right: 0,
    bottom: 0,
    background: "rgba(0,0,0,0.45)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 10000,
  };

  const box = {
    width: 420,
    maxWidth: "90%",
    background: "#fff",
    borderRadius: 8,
    padding: 20,
    boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
  };

  const footer = { display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 16 };

  return (
    <div style={overlay} role="dialog" aria-modal="true">
      <div style={box}>
        <h3 style={{ margin: "0 0 8px 0" }}>{title}</h3>
        <div style={{ color: "#374151", fontSize: 14 }}>{message}</div>
        <div style={footer}>
          <button onClick={onCancel} style={{ padding: "8px 12px", borderRadius: 6, border: "1px solid #e5e7eb", background: "#fff", cursor: "pointer" }}>
            {cancelLabel}
          </button>
          <button onClick={onConfirm} style={{ padding: "8px 12px", borderRadius: 6, border: "none", background: "#ef4444", color: "#fff", cursor: "pointer", fontWeight: 600 }}>
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
