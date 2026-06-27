import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useLanguage } from "../contexts/LanguageContext";
import ChatScreen from "../components/Chat/ChatScreen";
import TaskList from "../components/Progress/TaskList";
import ProgressBar from "../components/Progress/ProgressBar";
import ProficiencyTestModal from "../components/Profile/ProficiencyTestModal";
import { getSessionSummary } from "../services/api";
import { useInactivityLogout } from "../hooks/useInactivityLogout";

export default function OnboardingPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { lang, setLang, t } = useLanguage();
  const [selectedTask, setSelectedTask] = useState(null);
  const [activeTab, setActiveTab] = useState("chat");
  const [testNote, setTestNote] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [summaryModal, setSummaryModal] = useState({ open: false, text: "", loading: false, forLogout: false });

  useInactivityLogout(logout);

  if (!user) { navigate("/login"); return null; }

  const handleTaskCompleted = () => {
    setRefreshKey((k) => k + 1);
    setSelectedTask(null);
    setActiveTab("tasks");
  };

  const handleShowSummary = async (forLogout = false) => {
    setSummaryModal({ open: true, text: "", loading: true, forLogout });
    try {
      const data = await getSessionSummary();
      setSummaryModal({ open: true, text: data.summary, loading: false, forLogout });
    } catch {
      setSummaryModal({ open: true, text: t("summary.error"), loading: false, forLogout });
    }
  };

  return (
    <div style={styles.app}>
      <aside style={styles.sidebar}>
        <div style={styles.logoArea}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <h2 style={styles.logo}>🚀 OnboardAI</h2>
            <button style={styles.langBtn} onClick={() => setLang(lang === "en" ? "tr" : "en")}>
              {lang === "en" ? "🇹🇷 TR" : "🇬🇧 EN"}
            </button>
          </div>
          <p style={styles.userName}>{user.first_name} {user.last_name}</p>
          <p style={styles.userMeta}>{user.area} · {user.experience_level}</p>
        </div>

        <ProgressBar key={refreshKey} refreshKey={refreshKey} onShowSummary={() => handleShowSummary(false)} />

        {user.notes?.length > 0 && (
          <div style={styles.notesSection}>
            <p style={styles.notesTitle}>{t("sidebar.profileNotes")}</p>
            {user.notes.map((n, i) => (
              <div key={i} style={styles.noteItem}>
                <span>{n.value}</span>
                {!n.verified && (
                  <button style={styles.contestBtn} onClick={() => setTestNote(n.key)}>
                    {t("sidebar.contest")}
                  </button>
                )}
                {n.verified && <span style={styles.verifiedBadge}>{t("sidebar.verified")}</span>}
              </div>
            ))}
          </div>
        )}

        <button style={styles.logoutBtn} onClick={() => handleShowSummary(true)}>
          {t("sidebar.signOut")}
        </button>
      </aside>

      <main style={styles.main}>
        <div style={styles.tabs}>
          {["chat", "tasks"].map((tab) => (
            <button
              key={tab}
              style={{ ...styles.tab, ...(activeTab === tab ? styles.tabActive : {}) }}
              onClick={() => setActiveTab(tab)}
            >
              {tab === "chat" ? t("tabs.assistant") : t("tabs.tasks")}
            </button>
          ))}
          {selectedTask && (
            <span style={styles.taskBadge}>{t("tabs.activeTask")} {selectedTask.title}</span>
          )}
        </div>

        <div style={styles.content}>
          {activeTab === "chat" && (
            <ChatScreen
              user={user}
              currentTaskId={selectedTask?.id}
              currentTask={selectedTask}
              onTaskCompleted={handleTaskCompleted}
            />
          )}
          {activeTab === "tasks" && (
            <TaskList
              key={refreshKey}
              onSelectTask={(task) => { setSelectedTask(task); setActiveTab("chat"); }}
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

      {summaryModal.open && (
        <div style={styles.overlay}>
          <div style={styles.modal}>
            <h3 style={styles.modalTitle}>{t("summary.title")}</h3>
            {summaryModal.loading ? (
              <p style={styles.modalLoading}>{t("summary.loading")}</p>
            ) : (
              <div style={styles.summaryBox}>{summaryModal.text}</div>
            )}
            <div style={styles.modalActions}>
              <button
                style={styles.modalCloseBtn}
                onClick={() => setSummaryModal({ open: false, text: "", loading: false, forLogout: false })}
                disabled={summaryModal.loading}
              >
                {t("summary.close")}
              </button>
              {summaryModal.forLogout && (
                <button style={styles.modalLogoutBtn} onClick={logout} disabled={summaryModal.loading}>
                  {t("summary.signOut")}
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  app: { display: "flex", height: "100vh", overflow: "hidden" },
  sidebar: { width: 280, background: "#1e1b4b", color: "#fff", padding: 20, display: "flex", flexDirection: "column", gap: 12, overflowY: "auto" },
  logoArea: { marginBottom: 8 },
  logo: { fontSize: 20, fontWeight: 800, marginBottom: 4, margin: 0 },
  langBtn: { padding: "3px 8px", background: "rgba(255,255,255,0.15)", border: "1px solid rgba(255,255,255,0.25)", borderRadius: 6, cursor: "pointer", fontSize: 11, fontWeight: 700, color: "#fff" },
  userName: { fontSize: 14, fontWeight: 600, opacity: 0.9, marginTop: 6 },
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
  overlay: { position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 100 },
  modal: { background: "#fff", borderRadius: 16, padding: 28, width: "90%", maxWidth: 560, maxHeight: "80vh", display: "flex", flexDirection: "column", gap: 16 },
  modalTitle: { fontSize: 18, fontWeight: 700, margin: 0 },
  modalLoading: { color: "#6b7280", textAlign: "center", padding: "20px 0" },
  summaryBox: { flex: 1, overflowY: "auto", background: "#f0fdf4", borderRadius: 10, padding: 16, fontSize: 14, lineHeight: 1.7, whiteSpace: "pre-wrap", color: "#1f2937" },
  modalActions: { display: "flex", gap: 10, justifyContent: "flex-end" },
  modalCloseBtn: { padding: "10px 20px", background: "#f3f4f6", border: "1px solid #d1d5db", borderRadius: 8, cursor: "pointer", fontSize: 14, fontWeight: 600 },
  modalLogoutBtn: { padding: "10px 20px", background: "#dc2626", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 14, fontWeight: 700 },
};
