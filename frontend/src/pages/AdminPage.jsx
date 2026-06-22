import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import AdminPanel from "../components/Admin/AdminPanel";

export default function AdminPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  if (!user || user.role !== "admin") { navigate("/login"); return null; }

  return (
    <div style={styles.app}>
      <header style={styles.header}>
        <h1 style={styles.logo}>🚀 OnboardAI</h1>
        <div style={styles.right}>
          <span style={styles.adminBadge}>Admin</span>
          <button style={styles.logoutBtn} onClick={logout}>Çıkış</button>
        </div>
      </header>
      <AdminPanel />
    </div>
  );
}

const styles = {
  app: { minHeight: "100vh", background: "#f0f4ff" },
  header: { background: "#1e1b4b", color: "#fff", padding: "14px 24px", display: "flex", justifyContent: "space-between", alignItems: "center" },
  logo: { fontSize: 20, fontWeight: 800 },
  right: { display: "flex", alignItems: "center", gap: 12 },
  adminBadge: { background: "#f59e0b", color: "#000", padding: "3px 10px", borderRadius: 12, fontSize: 12, fontWeight: 700 },
  logoutBtn: { padding: "6px 14px", background: "rgba(255,255,255,0.1)", color: "#fff", border: "1px solid rgba(255,255,255,0.2)", borderRadius: 6, cursor: "pointer" },
};
