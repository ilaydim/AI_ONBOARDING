import React, { useEffect, useState } from "react";
import { getLearningPath } from "../../services/api";
import { useLanguage } from "../../contexts/LanguageContext";

export default function ProgressBar({ onShowSummary, refreshKey }) {
  const [stats, setStats] = useState(null);
  const { t } = useLanguage();

  useEffect(() => {
    getLearningPath().then((path) => {
      const completed = path.filter(({ status }) => status === "completed").length;
      const skipped = path.filter(({ status }) => status === "skipped").length;
      const pending = path.filter(({ status }) => status === "pending" || status === "in_progress").length;
      const total = path.length;
      const pct = total > 0 ? Math.round((completed / total) * 1000) / 10 : 0;
      setStats({ completed, skipped, pending, total, completion_percentage: pct });
    }).catch(() => {});
  }, [refreshKey]);

  if (!stats) return null;
  const pct = stats.completion_percentage || 0;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <span style={styles.label}>{t("progress.title")}</span>
        <span style={styles.pct}>{pct}%</span>
      </div>
      <div style={styles.barBg}>
        <div style={{ ...styles.barFill, width: `${pct}%` }} />
      </div>
      <div style={styles.counts}>
        <span>✅ {stats.completed} {t("progress.completed")}</span>
        <span>⏭ {stats.skipped} {t("progress.skipped")}</span>
        <span>⏳ {stats.pending} {t("progress.pending")}</span>
      </div>
      {onShowSummary && (
        <button style={styles.summaryBtn} onClick={onShowSummary}>
          {t("progress.summaryBtn")}
        </button>
      )}
    </div>
  );
}

const styles = {
  container: { background: "#fff", borderRadius: 12, padding: 16, border: "1px solid #e5e7eb", marginBottom: 12 },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 },
  label: { fontWeight: 700, fontSize: 14 },
  pct: { fontWeight: 700, fontSize: 20, color: "#4f46e5" },
  barBg: { height: 8, background: "#e5e7eb", borderRadius: 4, marginBottom: 10 },
  barFill: { height: "100%", background: "#4f46e5", borderRadius: 4, transition: "width 0.5s" },
  counts: { display: "flex", gap: 16, fontSize: 12, color: "#6b7280", marginBottom: 12 },
  summaryBtn: { width: "100%", padding: "8px 14px", background: "#10b981", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 13, fontWeight: 600 },
};
