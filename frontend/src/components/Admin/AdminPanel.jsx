import React, { useState, useEffect } from "react";
import { createUser, getUsers, getAdminProgress, deleteUser } from "../../services/api";
import { useLanguage } from "../../contexts/LanguageContext";

const AREAS = ["backend", "frontend", "devops", "product", "qa"];
const LEVELS = ["junior", "mid", "senior"];

function CreateUserForm() {
  const { t } = useLanguage();
  const [form, setForm] = useState({
    first_name: "", last_name: "", username: "", password: "",
    area: "backend", experience_level: "junior", language: "en",
    role: "employee", notes: [],
  });
  const [noteInput, setNoteInput] = useState({ key: "", value: "" });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const addNote = () => {
    if (!noteInput.key || !noteInput.value) return;
    setForm({ ...form, notes: [...form.notes, { ...noteInput, verified: false }] });
    setNoteInput({ key: "", value: "" });
  };

  const removeNote = (i) => setForm({ ...form, notes: form.notes.filter((_, idx) => idx !== i) });

  const handleCreate = async () => {
    setLoading(true);
    setMessage("");
    try {
      await createUser(form);
      setMessage(`✅ ${t("admin.createSuccess", { username: form.username })}`);
      setForm({ first_name: "", last_name: "", username: "", password: "", area: "backend", experience_level: "junior", language: "en", role: "employee", notes: [] });
    } catch (e) {
      setMessage(`❌ ${e.response?.data?.detail || t("admin.createError")}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={s.section}>
      <h3 style={s.sectionTitle}>{t("admin.createTitle")}</h3>
      <div style={s.grid}>
        {[["first_name", t("admin.firstName")], ["last_name", t("admin.lastName")], ["username", t("admin.username")], ["password", t("admin.password")]].map(([k, label]) => (
          <input key={k} style={s.input} placeholder={label} type={k === "password" ? "password" : "text"}
            value={form[k]} onChange={(e) => setForm({ ...form, [k]: e.target.value })} />
        ))}
      </div>
      <div style={s.row}>
        <select style={s.select} value={form.area} onChange={(e) => setForm({ ...form, area: e.target.value })}>
          {AREAS.map((a) => <option key={a} value={a}>{a}</option>)}
        </select>
        <select style={s.select} value={form.experience_level} onChange={(e) => setForm({ ...form, experience_level: e.target.value })}>
          {LEVELS.map((l) => <option key={l} value={l}>{l}</option>)}
        </select>
        <select style={s.select} value={form.language} onChange={(e) => setForm({ ...form, language: e.target.value })}>
          <option value="en">{t("admin.langEn")}</option>
          <option value="tr">{t("admin.langTr")}</option>
        </select>
        <select style={s.select} value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
          <option value="employee">{t("admin.roleEmployee")}</option>
          <option value="admin">{t("admin.roleAdmin")}</option>
        </select>
      </div>
      <div style={s.noteSection}>
        <p style={{ fontWeight: 600, marginBottom: 8 }}>{t("admin.profileNotes")}</p>
        <div style={s.row}>
          <input style={s.input} placeholder={t("admin.noteKey")} value={noteInput.key}
            onChange={(e) => setNoteInput({ ...noteInput, key: e.target.value })} />
          <input style={s.input} placeholder={t("admin.noteValue")} value={noteInput.value}
            onChange={(e) => setNoteInput({ ...noteInput, value: e.target.value })} />
          <button style={s.addBtn} onClick={addNote}>{t("admin.addNote")}</button>
        </div>
        {form.notes.map((n, i) => (
          <div key={i} style={s.noteTag}>
            <strong>{n.key}</strong>: {n.value}
            <button style={s.removeBtn} onClick={() => removeNote(i)}>×</button>
          </div>
        ))}
      </div>
      {message && <p style={{ marginBottom: 12, color: message.startsWith("✅") ? "#10b981" : "#dc2626" }}>{message}</p>}
      <button style={s.createBtn} onClick={handleCreate} disabled={loading}>
        {loading ? t("admin.creating") : t("admin.createBtn")}
      </button>
    </div>
  );
}

function EmployeeDetail({ employee, onBack }) {
  const { t } = useLanguage();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getAdminProgress(employee.id)
      .then(setReport)
      .catch(() => setError(t("admin.loadError")))
      .finally(() => setLoading(false));
  }, [employee.id]);

  if (loading) return <p style={{ padding: 16, color: "#666" }}>{t("admin.loading")}</p>;
  if (error) return <p style={{ padding: 16, color: "red" }}>{error}</p>;

  const { stats, gaps, proficiency_tests } = report;
  const pct = stats?.completion_percentage ?? 0;

  return (
    <div>
      <button style={s.backBtn} onClick={onBack}>{t("admin.back")}</button>
      <h3 style={s.sectionTitle}>
        {employee.first_name} {employee.last_name}
        <span style={s.areaBadge}>{employee.area}</span>
        <span style={s.levelBadge}>{employee.experience_level}</span>
      </h3>

      <div style={s.card}>
        <p style={s.cardTitle}>{t("admin.progressTitle")}</p>
        <div style={s.barBg}><div style={{ ...s.barFill, width: `${pct}%` }} /></div>
        <p style={s.pctLabel}>{t("admin.pctComplete", { pct })}</p>
        <div style={s.statsRow}>
          <span>✅ {stats?.completed ?? 0} {t("progress.completed")}</span>
          <span>⏭ {stats?.skipped ?? 0} {t("progress.skipped")}</span>
          <span>⏳ {stats?.pending ?? 0} {t("progress.pending")}</span>
        </div>
      </div>

      <div style={s.card}>
        <p style={s.cardTitle}>{t("admin.gapsTitle")}</p>
        {gaps && gaps.length > 0 ? (
          <table style={s.table}>
            <thead><tr>
              <th style={s.th}>{t("admin.gapTopic")}</th>
              <th style={s.th}>{t("admin.gapSignal")}</th>
              <th style={s.th}>{t("admin.gapCount")}</th>
            </tr></thead>
            <tbody>
              {gaps.map((g, i) => (
                <tr key={i}>
                  <td style={s.td}><strong>{g.topic}</strong></td>
                  <td style={s.td}>{g.signal}</td>
                  <td style={{ ...s.td, textAlign: "center" }}><span style={s.countBadge}>{g.count}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : <p style={s.emptyText}>{t("admin.noGaps")}</p>}
      </div>

      <div style={s.card}>
        <p style={s.cardTitle}>{t("admin.testsTitle")}</p>
        {proficiency_tests && proficiency_tests.length > 0 ? (
          <table style={s.table}>
            <thead><tr>
              <th style={s.th}>{t("admin.testTopic")}</th>
              <th style={s.th}>{t("admin.testStatus")}</th>
              <th style={s.th}>{t("admin.testAttempts")}</th>
              <th style={s.th}>{t("admin.testFailed")}</th>
              <th style={s.th}>{t("admin.testScore")}</th>
            </tr></thead>
            <tbody>
              {proficiency_tests.map((tt, i) => (
                <tr key={i}>
                  <td style={s.td}><strong>{tt.note_key}</strong></td>
                  <td style={s.td}>
                    {tt.passed
                      ? <span style={{ color: "#10b981", fontWeight: 700 }}>{t("admin.testPassed")}</span>
                      : <span style={{ color: "#ef4444", fontWeight: 700 }}>{t("admin.testFail")}</span>}
                  </td>
                  <td style={{ ...s.td, textAlign: "center" }}>{tt.attempts}</td>
                  <td style={{ ...s.td, textAlign: "center" }}>
                    {tt.failed_attempts > 0 ? <span style={s.failBadge}>{tt.failed_attempts}</span> : "—"}
                  </td>
                  <td style={{ ...s.td, textAlign: "center" }}>{tt.last_score}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : <p style={s.emptyText}>{t("admin.noTests")}</p>}
      </div>

      {employee.notes?.length > 0 && (
        <div style={s.card}>
          <p style={s.cardTitle}>{t("admin.notesTitle")}</p>
          {employee.notes.map((n, i) => (
            <div key={i} style={s.noteRow}>
              <span><strong>{n.key}</strong>: {n.value}</span>
              {n.verified
                ? <span style={s.verifiedTag}>{t("admin.noteVerified")}</span>
                : <span style={s.pendingTag}>{t("admin.notePending")}</span>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function EmployeeReports() {
  const { t } = useLanguage();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [deleting, setDeleting] = useState(null);

  const loadUsers = () => {
    setLoading(true);
    getUsers()
      .then((all) => setUsers(all.filter((u) => u.role !== "admin")))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => { loadUsers(); }, []);

  const handleDelete = async (u) => {
    if (!window.confirm(t("admin.deleteConfirm", { name: `${u.first_name} ${u.last_name}` }))) return;
    setDeleting(u.id);
    try {
      await deleteUser(u.id);
      loadUsers();
    } catch (e) {
      alert(e.response?.data?.detail || t("admin.deleteError"));
    } finally {
      setDeleting(null);
    }
  };

  if (loading) return <p style={{ padding: 16, color: "#666" }}>{t("admin.loading")}</p>;
  if (selected) return <EmployeeDetail employee={selected} onBack={() => setSelected(null)} />;

  return (
    <div style={s.section}>
      <h3 style={s.sectionTitle}>{t("admin.reportsList")}</h3>
      {users.length === 0 ? (
        <p style={s.emptyText}>{t("admin.noEmployees")}</p>
      ) : (
        <table style={s.table}>
          <thead><tr>
            <th style={s.th}>{t("admin.reportsName")}</th>
            <th style={s.th}>{t("admin.reportsUsername")}</th>
            <th style={s.th}>{t("admin.reportsArea")}</th>
            <th style={s.th}>{t("admin.reportsLevel")}</th>
            <th style={s.th}></th>
          </tr></thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} style={{ borderBottom: "1px solid #f3f4f6" }}>
                <td style={s.td}>{u.first_name} {u.last_name}</td>
                <td style={s.td}>{u.username}</td>
                <td style={s.td}><span style={s.areaBadge}>{u.area}</span></td>
                <td style={s.td}><span style={s.levelBadge}>{u.experience_level}</span></td>
                <td style={s.td}>
                  <div style={{ display: "flex", gap: 8 }}>
                    <button style={s.detailBtn} onClick={() => setSelected(u)}>
                      {t("admin.viewReport")}
                    </button>
                    <button
                      style={s.deleteBtn}
                      onClick={() => handleDelete(u)}
                      disabled={deleting === u.id}
                    >
                      {deleting === u.id ? "…" : t("admin.deleteUser")}
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default function AdminPanel() {
  const { t } = useLanguage();
  const [tab, setTab] = useState("create");

  return (
    <div style={s.container}>
      <div style={s.tabs}>
        {[["create", t("admin.tabCreate")], ["reports", t("admin.tabReports")]].map(([key, label]) => (
          <button
            key={key}
            style={{ ...s.tab, ...(tab === key ? s.tabActive : {}) }}
            onClick={() => setTab(key)}
          >
            {label}
          </button>
        ))}
      </div>
      {tab === "create" ? <CreateUserForm /> : <EmployeeReports />}
    </div>
  );
}

const s = {
  container: { padding: 24, maxWidth: 900, margin: "0 auto" },
  tabs: { display: "flex", gap: 4, marginBottom: 20, borderBottom: "2px solid #e5e7eb", paddingBottom: 0 },
  tab: { padding: "10px 20px", border: "none", background: "none", cursor: "pointer", fontSize: 14, fontWeight: 600, color: "#6b7280", borderBottom: "2px solid transparent", marginBottom: -2 },
  tabActive: { color: "#4f46e5", borderBottom: "2px solid #4f46e5" },
  section: { background: "#fff", borderRadius: 12, padding: 24, border: "1px solid #e5e7eb" },
  sectionTitle: { fontWeight: 700, marginBottom: 16, fontSize: 16, display: "flex", alignItems: "center", gap: 8 },
  grid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 12 },
  row: { display: "flex", gap: 10, marginBottom: 12, flexWrap: "wrap" },
  input: { flex: 1, padding: "10px 12px", border: "1px solid #ddd", borderRadius: 8, fontSize: 14, minWidth: 120 },
  select: { flex: 1, padding: "10px 12px", border: "1px solid #ddd", borderRadius: 8, fontSize: 14, minWidth: 100 },
  noteSection: { marginBottom: 16 },
  noteTag: { display: "inline-flex", alignItems: "center", gap: 6, background: "#f3f4f6", padding: "4px 10px", borderRadius: 20, marginRight: 8, marginBottom: 6, fontSize: 13 },
  addBtn: { padding: "10px 16px", background: "#4f46e5", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer" },
  removeBtn: { background: "none", border: "none", cursor: "pointer", color: "#dc2626", fontWeight: 700 },
  createBtn: { padding: "12px 24px", background: "#10b981", color: "#fff", border: "none", borderRadius: 8, fontSize: 15, fontWeight: 700, cursor: "pointer" },
  backBtn: { padding: "6px 14px", background: "#f3f4f6", border: "1px solid #ddd", borderRadius: 8, cursor: "pointer", marginBottom: 16, fontSize: 13 },
  card: { background: "#fff", borderRadius: 12, padding: 20, border: "1px solid #e5e7eb", marginBottom: 16 },
  cardTitle: { fontWeight: 700, fontSize: 14, marginBottom: 12, color: "#374151" },
  barBg: { height: 10, background: "#e5e7eb", borderRadius: 5, marginBottom: 6 },
  barFill: { height: "100%", background: "#4f46e5", borderRadius: 5, transition: "width 0.5s" },
  pctLabel: { fontSize: 13, fontWeight: 700, color: "#4f46e5", marginBottom: 8 },
  statsRow: { display: "flex", gap: 20, fontSize: 13, color: "#6b7280" },
  table: { width: "100%", borderCollapse: "collapse" },
  th: { textAlign: "left", padding: "8px 10px", fontSize: 12, fontWeight: 700, color: "#6b7280", borderBottom: "1px solid #e5e7eb", textTransform: "uppercase" },
  td: { padding: "10px 10px", fontSize: 14, verticalAlign: "middle" },
  emptyText: { color: "#9ca3af", fontSize: 14 },
  countBadge: { background: "#fef3c7", color: "#92400e", padding: "2px 8px", borderRadius: 12, fontSize: 12, fontWeight: 700 },
  failBadge: { background: "#fee2e2", color: "#991b1b", padding: "2px 8px", borderRadius: 12, fontSize: 12, fontWeight: 700 },
  areaBadge: { background: "#ede9fe", color: "#5b21b6", padding: "2px 8px", borderRadius: 12, fontSize: 12, fontWeight: 600 },
  levelBadge: { background: "#e0f2fe", color: "#0369a1", padding: "2px 8px", borderRadius: 12, fontSize: 12, fontWeight: 600 },
  detailBtn: { padding: "6px 12px", background: "#4f46e5", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer", fontSize: 13, fontWeight: 600 },
  deleteBtn: { padding: "6px 12px", background: "#fee2e2", color: "#dc2626", border: "1px solid #fca5a5", borderRadius: 6, cursor: "pointer", fontSize: 13, fontWeight: 600 },
  noteRow: { display: "flex", justifyContent: "space-between", alignItems: "center", padding: "6px 0", borderBottom: "1px solid #f3f4f6", fontSize: 13 },
  verifiedTag: { color: "#10b981", fontWeight: 700, fontSize: 12 },
  pendingTag: { color: "#f59e0b", fontWeight: 700, fontSize: 12 },
};
