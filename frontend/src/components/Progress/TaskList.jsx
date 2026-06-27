import React, { useEffect, useState } from "react";
import { getLearningPath, skipTask, resumeTask } from "../../services/api";
import { useLanguage } from "../../contexts/LanguageContext";

const STATUS_COLOR = {
  pending: "#f59e0b",
  in_progress: "#4f46e5",
  completed: "#10b981",
  skipped: "#9ca3af",
};

export default function TaskList({ onSelectTask, selectedTaskId }) {
  const [path, setPath] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { t } = useLanguage();

  const load = async () => {
    try {
      const data = await getLearningPath();
      setPath(data);
    } catch {
      setError(t("tasks.loadError"));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleSkip = async (taskId, e) => {
    e.stopPropagation();
    try {
      await skipTask(taskId);
      load();
    } catch (err) {
      alert(err.response?.data?.detail || t("tasks.skipError"));
    }
  };

  const handleResume = async (taskId, e) => {
    e.stopPropagation();
    try {
      await resumeTask(taskId);
      load();
    } catch (err) {
      alert(err.response?.data?.detail || t("tasks.resumeError"));
    }
  };

  const handleSelect = (task, locked) => {
    if (locked) { alert(t("tasks.lockedAlert")); return; }
    onSelectTask?.(task);
  };

  if (loading) return <p style={{ padding: 16, color: "#666" }}>{t("tasks.loading")}</p>;
  if (error) return <p style={{ padding: 16, color: "red" }}>{error}</p>;

  const activeIdx = path.findIndex(({ status }) => status !== "completed" && status !== "skipped");
  const completed = path.filter(({ status }) => status === "completed").length;
  const skipped = path.filter(({ status }) => status === "skipped").length;
  const pending = path.filter(({ status }) => status === "pending").length;
  const allDone = path.length > 0 && pending === 0;

  return (
    <div style={styles.container}>
      {allDone && (
        <div style={styles.completionBanner}>
          <span style={{ fontSize: 28 }}>🎉</span>
          <div>
            <p style={styles.completionTitle}>{t("tasks.allDoneTitle")}</p>
            <p style={styles.completionSub}>{t("tasks.allDoneSub")}</p>
          </div>
        </div>
      )}
      <h3 style={styles.title}>{t("tasks.title")}</h3>
      <div style={styles.statsRow}>
        <span>✅ {completed} {t("tasks.status.completed").replace("✅ ", "")}</span>
        <span>⏭ {skipped} {t("tasks.status.skipped").replace("⏭ ", "")}</span>
        <span>⏳ {pending} {t("tasks.status.pending")}</span>
      </div>
      {path.map(({ task, status }, idx) => {
        const locked = status === "pending" && idx > activeIdx && activeIdx !== -1;
        return (
          <div
            key={task.id}
            style={{
              ...styles.card,
              borderLeft: `4px solid ${locked ? "#d1d5db" : STATUS_COLOR[status]}`,
              background: selectedTaskId === task.id ? "#f0f4ff" : locked ? "#fafafa" : "#fff",
              cursor: locked ? "not-allowed" : "pointer",
              opacity: locked ? 0.6 : 1,
            }}
            onClick={() => handleSelect(task, locked)}
          >
            <div style={styles.row}>
              <span style={{ ...styles.index, background: locked ? "#e5e7eb" : undefined }}>
                {locked ? "🔒" : idx + 1}
              </span>
              <div style={{ flex: 1 }}>
                <p style={styles.taskTitle}>{task.title}</p>
                <p style={styles.meta}>
                  ~{task.estimated_hours}{t("tasks.hours")} · {t(`tasks.status.${status}`)}
                  {task.skippable && status === "pending" && !locked && (
                    <button style={styles.skipBtn} onClick={(e) => handleSkip(task.id, e)}>
                      {t("tasks.skip")}
                    </button>
                  )}
                  {status === "skipped" && (
                    <button style={styles.resumeBtn} onClick={(e) => handleResume(task.id, e)}>
                      {t("tasks.resume")}
                    </button>
                  )}
                </p>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

const styles = {
  container: { padding: 12 },
  title: { fontWeight: 700, marginBottom: 8, fontSize: 15 },
  statsRow: { display: "flex", gap: 16, fontSize: 12, color: "#6b7280", marginBottom: 12, padding: "8px 10px", background: "#f9fafb", borderRadius: 8 },
  card: { padding: "12px 14px", marginBottom: 8, borderRadius: 8, boxShadow: "0 1px 4px rgba(0,0,0,0.06)" },
  row: { display: "flex", alignItems: "flex-start", gap: 10 },
  index: { width: 24, height: 24, background: "#e5e7eb", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 700, flexShrink: 0 },
  taskTitle: { fontWeight: 600, fontSize: 14, marginBottom: 2 },
  meta: { fontSize: 12, color: "#6b7280" },
  skipBtn: { marginLeft: 10, padding: "2px 8px", fontSize: 11, background: "#f3f4f6", border: "1px solid #ddd", borderRadius: 4, cursor: "pointer" },
  resumeBtn: { marginLeft: 10, padding: "2px 8px", fontSize: 11, background: "#dbeafe", border: "1px solid #93c5fd", borderRadius: 4, cursor: "pointer", color: "#1d4ed8", fontWeight: 600 },
  completionBanner: { display: "flex", gap: 12, alignItems: "center", background: "linear-gradient(135deg,#d1fae5,#a7f3d0)", border: "2px solid #10b981", borderRadius: 12, padding: "16px 20px", marginBottom: 16 },
  completionTitle: { fontWeight: 800, fontSize: 16, color: "#065f46", margin: 0 },
  completionSub: { fontSize: 12, color: "#047857", margin: "4px 0 0" },
};
