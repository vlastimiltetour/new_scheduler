import React, { useState, useEffect } from "react";

export default function UserModal({
  isOpen,
  onClose,
  onConfirm,
  mode,
  initialData,
}) {
  const [formData, setFormData] = useState({
    id: "",
    name: "",
    email: "",
    person_type: "candidate",
  });

  useEffect(() => {
    if (initialData) {
      setFormData({
        id: initialData.id || "",
        name: initialData.name || "",
        email: initialData.email || "",
        person_type: initialData.person_type || "candidate",
      });
    } else {
      setFormData({ id: "", name: "", person_type: "candidate", email: "" });
    }
  }, [initialData, isOpen]);

  if (!isOpen) return null;

  const isReadOnly = mode === "DETAIL" || mode === "DELETE";

  return (
    <div style={styles.modalOverlay} onClick={onClose}>
      {/* stopPropagation zabrání zavření při kliknutí do okna */}
      <div style={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        <h2 style={styles.heading}>
          {mode === "ADD" && "Add User"}
          {mode === "DETAIL" && "User Detail"}
          {mode === "UPDATE" && "Update User"}
          {mode === "DELETE" && "Delete User"}
        </h2>

          {mode === "DELETE" && (
            <p style={{ color: "#e11d48", fontWeight: "bold", marginBottom: "16px" }}>
              Are you sure you want to delete this user?
            </p>
          )}

        <div style={styles.form}>
          <div>
            <label style={styles.label}>ID</label>
            <input
              style={styles.input}
              disabled={true}
              value={formData.id}
              onChange={(e) => setFormData({ ...formData, id: e.target.value })}
            />
          </div>

          <div>
            <label style={styles.label}>Name</label>
            <input
              style={styles.input}
              disabled={isReadOnly}
              value={formData.name}
              onChange={(e) =>
                setFormData({ ...formData, name: e.target.value })
              }
            />
          </div>

          <div>
            <label style={styles.label}>Role</label>
            <select
              style={styles.input}
              disabled={isReadOnly}
              value={formData.person_type}
              onChange={(e) =>
                setFormData({ ...formData, person_type: e.target.value })
              }
              >
              <option value="candidate">candidate</option>
              <option value="interviewer">interviewer</option>
            </select>
              
          </div>

          <div>
            <label style={styles.label}>Email</label>
            <input
              style={styles.input}
              disabled={isReadOnly}
              value={formData.email}
              onChange={(e) =>
                setFormData({ ...formData, email: e.target.value })
              }
            />
          </div>
        </div>

        <div style={styles.modalActions}>
          <button
            style={{ ...styles.actionBtn, ...styles.closeBtn }}
            onClick={onClose}
          >
            Close
          </button>
          <button
            style={{ ...styles.actionBtn, ...styles.confirmBtn }}
            onClick={() => onConfirm(formData)}
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  modalOverlay: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100vw",
    height: "100vh",
    backgroundColor: "rgba(0, 0, 0, 0.75)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 99999,
  },
  modalContent: {
    backgroundColor: "#1f2937",
    padding: "24px",
    borderRadius: "8px",
    width: "350px",
    border: "1px solid #374151",
  },
  heading: { marginTop: 0, marginBottom: "10px", color: "#ffffff", fontSize: "18px" },
  form: { display: "flex", flexDirection: "column", gap: "12px" },
  label: {
    display: "block",
    color: "#9ca3af",
    fontSize: "12px",
    marginBottom: "4px",
  },
  input: {
    width: "100%",
    padding: "8px",
    borderRadius: "4px",
    border: "1px solid #374151",
    backgroundColor: "#111827",
    color: "#fff",
    boxSizing: "border-box",
  },
  modalActions: {
    display: "flex",
    justifyContent: "flex-end",
    gap: "8px",
    marginTop: "20px",
  },
  closeBtn: {
    padding: "8px 14px",
    border: "none",
    borderRadius: "4px",
    backgroundColor: "#374151",
    color: "#fff",
    cursor: "pointer",
    minWidth: '64px'
  },
  confirmBtn: {
    padding: "8px 14px",
    border: "none",
    borderRadius: "4px",
    color: "#374151",
    cursor: "pointer",
    minWidth: '64px'
  },
};
