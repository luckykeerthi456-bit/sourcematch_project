import React, { useEffect, useState } from "react";
import axios from "axios";

export default function SettingsPanel({ API, user, setMessage }) {
  const [skillThreshold, setSkillThreshold] = useState(0.62);
  const [inputValue, setInputValue] = useState(String(0.62));
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  const canModify = user && (user.role === "recruiter" || user.role === "admin");

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const res = await axios.get(API + "/settings/skill_threshold");
        if (mounted && res && res.data && typeof res.data.skill_threshold !== "undefined") {
          setSkillThreshold(res.data.skill_threshold);
          setInputValue(String(res.data.skill_threshold));
          setError("");
        }
      } catch (e) {
        // non-fatal
        console.error("Failed to load skill threshold:", e);
      }
    })();
    return () => { mounted = false; };
  }, [API]);

  const validate = (v) => {
    if (v === null || v === undefined || v === "") return "Value is required";
    const n = Number(v);
    if (!isFinite(n)) return "Must be a number";
    if (n < 0 || n > 1) return "Must be between 0.0 and 1.0";
    return "";
  };

  const onChange = (v) => {
    setInputValue(v);
    setError(validate(v));
  };

  const onSave = async () => {
    const err = validate(inputValue);
    setError(err);
    if (err) {
      setMessage && setMessage("Please fix errors before saving");
      return;
    }
    const parsed = Number(inputValue);
    if (parsed === Number(skillThreshold)) {
      setMessage && setMessage("No changes to save");
      return;
    }
    try {
      setSaving(true);
      await axios.put(API + "/settings/skill_threshold", { skill_threshold: parsed });
      setSkillThreshold(parsed);
      setMessage && setMessage("Settings updated");
    } catch (e) {
      console.error("Failed to save skill threshold:", e);
      setMessage && setMessage(e?.response?.data?.detail || "Failed to update settings");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <h2>Settings</h2>
      <div style={{ maxWidth: 600, background: "#fff", padding: 20, borderRadius: 8, boxShadow: "0 2px 8px rgba(0,0,0,0.06)" }}>
        <label style={{ display: "block", marginBottom: 8, fontWeight: 600 }}>Skill similarity threshold (0.0 - 1.0)</label>
        <input
          value={inputValue}
          onChange={(e) => onChange(e.target.value)}
          type="number"
          step="0.01"
          min="0"
          max="1"
          style={{ width: "100%", padding: 8, marginBottom: 6 }}
        />
        {error && <p style={{ color: "#ef4444", margin: "0 0 8px 0", fontSize: 13 }}>{error}</p>}

        <div style={{ display: "flex", gap: 8 }}>
          <button
            onClick={onSave}
            disabled={Boolean(error) || saving || Number(inputValue) === Number(skillThreshold) || !canModify}
            title={!canModify ? "You don't have permission to modify settings" : undefined}
            style={{ padding: "10px 16px", background: (!canModify ? "#9ca3af" : "#667eea"), color: "#fff", border: "none", borderRadius: 6, cursor: (!canModify ? "not-allowed" : "pointer"), fontWeight: 700 }}
          >
            {saving ? "Saving..." : "Save"}
          </button>

          <button onClick={() => { setInputValue(String(skillThreshold)); setError(""); }} style={{ padding: "10px 16px", background: "#e5e7eb", border: "none", borderRadius: 6, cursor: "pointer" }}>
            Reset
          </button>
        </div>
      </div>
    </div>
  );
}
