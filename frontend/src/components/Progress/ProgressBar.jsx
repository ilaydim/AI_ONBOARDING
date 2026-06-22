import React, { useEffect, useState } from "react";
import { getMyProgress, getSessionSummary } from "../../services/api";

export default function ProgressBar() {
  const [stats, setStats] = useState(null);
  const [summary, setSummary] = useState("");
  const [loadingSummary, setLoadingSummary] = useState(false);

  useEffect(() => {
    getMyProgress().then(setStats).catch(() => {});
  }, []);

  const handleSummary = async () => {
    setLoadingSummary(true);
    try {
      const data = await getSessionSummary();
      setSummary(data.summary);
    } catch { setSummary("Özet üretilemedi."); }
    finally { setLoadingSummary(false); }
  };

  if (!stats) return null;
  const pct = stats.completion_percentage || 0;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <span style={styles.label}>Genel İlerleme</span>
        <span style={styles.pct}>{pct}%</span>
      </div>
      <div style={styles.barBg}>
        <div style={{ ...styles.barFill, width: `${pct}%` }} />
      </div>
      <div style={styles.counts}>
        <span>✅ {stats.completed} tamamlandı</span>
        <span>⏭ {stats.skipped} atlandı</span>
        <span>⏳ {stats.pending} bekliyor</span>
      </div>
      <button style={styles.summaryBtn} onClick={handleSummary} disabled={loadingSummary}>
        {loadingSummary ? "Özet hazırlanıyor..." : "Oturum Özeti Al"}
      </button>
      {summary && <div style={styles.summary}>{summary}</div>}
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
  summaryBtn: { padding: "8px 14px", background: "#10b981", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 13, fontWeight: 600 },
  summary: { marginTop: 12, padding: 12, background: "#f0fdf4", borderRadius: 8, fontSize: 13, lineHeight: 1.6, whiteSpace: "pre-wrap" },
};
