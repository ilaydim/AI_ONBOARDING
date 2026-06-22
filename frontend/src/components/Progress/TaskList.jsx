import React, { useEffect, useState } from "react";
import { getLearningPath, skipTask } from "../../services/api";

const STATUS_COLOR = {
  pending: "#f59e0b",
  in_progress: "#4f46e5",
  completed: "#10b981",
  skipped: "#9ca3af",
};

const STATUS_LABEL = {
  pending: "Bekliyor",
  in_progress: "Devam ediyor",
  completed: "✅ Tamamlandı",
  skipped: "⏭ Atlandı",
};

export default function TaskList({ onSelectTask, selectedTaskId }) {
  const [path, setPath] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    try {
      const data = await getLearningPath();
      setPath(data);
    } catch {
      setError("Öğrenme yolu yüklenemedi.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleSkip = async (taskId) => {
    try {
      await skipTask(taskId);
      load();
    } catch (e) {
      alert(e.response?.data?.detail || "Görev atlanamadı.");
    }
  };

  if (loading) return <p style={{ padding: 16, color: "#666" }}>Yükleniyor...</p>;
  if (error) return <p style={{ padding: 16, color: "red" }}>{error}</p>;

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Öğrenme Yolu</h3>
      {path.map(({ task, status }, idx) => (
        <div
          key={task.id}
          style={{
            ...styles.card,
            borderLeft: `4px solid ${STATUS_COLOR[status]}`,
            background: selectedTaskId === task.id ? "#f0f4ff" : "#fff",
          }}
          onClick={() => onSelectTask?.(task)}
        >
          <div style={styles.row}>
            <span style={styles.index}>{idx + 1}</span>
            <div style={{ flex: 1 }}>
              <p style={styles.taskTitle}>{task.title}</p>
              <p style={styles.meta}>
                ~{task.estimated_hours}s · {STATUS_LABEL[status]}
                {task.skippable && status === "pending" && (
                  <button
                    style={styles.skipBtn}
                    onClick={(e) => { e.stopPropagation(); handleSkip(task.id); }}
                  >
                    Atla
                  </button>
                )}
              </p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

const styles = {
  container: { padding: 12 },
  title: { fontWeight: 700, marginBottom: 12, fontSize: 15 },
  card: { padding: "12px 14px", marginBottom: 8, borderRadius: 8, cursor: "pointer", boxShadow: "0 1px 4px rgba(0,0,0,0.06)" },
  row: { display: "flex", alignItems: "flex-start", gap: 10 },
  index: { width: 24, height: 24, background: "#e5e7eb", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 700, flexShrink: 0 },
  taskTitle: { fontWeight: 600, fontSize: 14, marginBottom: 2 },
  meta: { fontSize: 12, color: "#6b7280" },
  skipBtn: { marginLeft: 10, padding: "2px 8px", fontSize: 11, background: "#f3f4f6", border: "1px solid #ddd", borderRadius: 4, cursor: "pointer" },
};
