import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import ChatScreen from "../components/Chat/ChatScreen";
import TaskList from "../components/Progress/TaskList";
import ProgressBar from "../components/Progress/ProgressBar";
import ProficiencyTestModal from "../components/Profile/ProficiencyTestModal";

export default function OnboardingPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [selectedTask, setSelectedTask] = useState(null);
  const [activeTab, setActiveTab] = useState("chat");
  const [testNote, setTestNote] = useState(null);

  if (!user) { navigate("/login"); return null; }

  return (
    <div style={styles.app}>
      {/* Sidebar */}
      <aside style={styles.sidebar}>
        <div style={styles.logoArea}>
          <h2 style={styles.logo}>🚀 OnboardAI</h2>
          <p style={styles.userName}>{user.first_name} {user.last_name}</p>
          <p style={styles.userMeta}>{user.area} · {user.experience_level}</p>
        </div>

        <ProgressBar />

        {/* Profil notları — itiraz butonu */}
        {user.notes?.length > 0 && (
          <div style={styles.notesSection}>
            <p style={styles.notesTitle}>Profil Notların</p>
            {user.notes.map((n, i) => (
              <div key={i} style={styles.noteItem}>
                <span>{n.value}</span>
                {!n.verified && (
                  <button style={styles.contestBtn} onClick={() => setTestNote(n.key)}>
                    İtiraz Et
                  </button>
                )}
                {n.verified && <span style={styles.verifiedBadge}>✓ Doğrulandı</span>}
              </div>
            ))}
          </div>
        )}

        <button style={styles.logoutBtn} onClick={logout}>Çıkış Yap</button>
      </aside>

      {/* Main */}
      <main style={styles.main}>
        {/* Tabs */}
        <div style={styles.tabs}>
          {["chat", "tasks"].map((tab) => (
            <button
              key={tab}
              style={{ ...styles.tab, ...(activeTab === tab ? styles.tabActive : {}) }}
              onClick={() => setActiveTab(tab)}
            >
              {tab === "chat" ? "💬 Asistan" : "📋 Görevler"}
            </button>
          ))}
          {selectedTask && <span style={styles.taskBadge}>Aktif Görev: {selectedTask.title}</span>}
        </div>

        <div style={styles.content}>
          {activeTab === "chat" && <ChatScreen user={user} currentTaskId={selectedTask?.id} />}
          {activeTab === "tasks" && (
            <TaskList
              onSelectTask={(t) => { setSelectedTask(t); setActiveTab("chat"); }}
              selectedTaskId={selectedTask?.id}
            />
          )}
        </div>
      </main>

      {testNote && (
        <ProficiencyTestModal
          noteKey={testNote}
          onClose={() => setTestNote(null)}
          onPassed={() => { setTestNote(null); window.location.reload(); }}
        />
      )}
    </div>
  );
}

const styles = {
  app: { display: "flex", height: "100vh", overflow: "hidden" },
  sidebar: { width: 280, background: "#1e1b4b", color: "#fff", padding: 20, display: "flex", flexDirection: "column", gap: 12, overflowY: "auto" },
  logoArea: { marginBottom: 8 },
  logo: { fontSize: 20, fontWeight: 800, marginBottom: 4 },
  userName: { fontSize: 14, fontWeight: 600, opacity: 0.9 },
  userMeta: { fontSize: 12, opacity: 0.6, textTransform: "capitalize" },
  notesSection: { background: "rgba(255,255,255,0.08)", borderRadius: 10, padding: 12 },
  notesTitle: { fontSize: 12, fontWeight: 700, marginBottom: 8, opacity: 0.7, textTransform: "uppercase" },
  noteItem: { fontSize: 12, marginBottom: 8, display: "flex", justifyContent: "space-between", alignItems: "center", gap: 6 },
  contestBtn: { padding: "3px 8px", background: "#f59e0b", color: "#000", border: "none", borderRadius: 4, cursor: "pointer", fontSize: 11, fontWeight: 700, flexShrink: 0 },
  verifiedBadge: { color: "#10b981", fontSize: 11, fontWeight: 700 },
  logoutBtn: { marginTop: "auto", padding: "10px", background: "rgba(255,255,255,0.1)", color: "#fff", border: "1px solid rgba(255,255,255,0.2)", borderRadius: 8, cursor: "pointer" },
  main: { flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" },
  tabs: { display: "flex", gap: 4, padding: "12px 16px", background: "#fff", borderBottom: "1px solid #e5e7eb", alignItems: "center" },
  tab: { padding: "8px 16px", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 14, background: "#f3f4f6", fontWeight: 600 },
  tabActive: { background: "#4f46e5", color: "#fff" },
  taskBadge: { marginLeft: "auto", fontSize: 12, color: "#4f46e5", fontWeight: 600 },
  content: { flex: 1, overflow: "hidden", padding: 16 },
};
