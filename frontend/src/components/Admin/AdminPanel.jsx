import React, { useState } from "react";
import { createUser } from "../../services/api";

const AREAS = ["backend", "frontend", "devops", "product", "qa"];
const LEVELS = ["junior", "mid", "senior"];

export default function AdminPanel() {
  const [form, setForm] = useState({
    first_name: "", last_name: "", username: "", password: "",
    area: "backend", experience_level: "junior", language: "tr",
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

  const removeNote = (i) => {
    setForm({ ...form, notes: form.notes.filter((_, idx) => idx !== i) });
  };

  const handleCreate = async () => {
    setLoading(true);
    setMessage("");
    try {
      await createUser(form);
      setMessage(`✅ Kullanıcı '${form.username}' oluşturuldu.`);
      setForm({ first_name: "", last_name: "", username: "", password: "", area: "backend", experience_level: "junior", language: "tr", role: "employee", notes: [] });
    } catch (e) {
      setMessage(`❌ ${e.response?.data?.detail || "Hata oluştu"}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Yönetici Paneli</h2>
      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>Yeni Çalışan Oluştur</h3>
        <div style={styles.grid}>
          {[["first_name", "Ad"], ["last_name", "Soyad"], ["username", "Kullanıcı Adı"], ["password", "Şifre"]].map(([k, label]) => (
            <input
              key={k}
              style={styles.input}
              placeholder={label}
              type={k === "password" ? "password" : "text"}
              value={form[k]}
              onChange={(e) => setForm({ ...form, [k]: e.target.value })}
            />
          ))}
        </div>
        <div style={styles.row}>
          <select style={styles.select} value={form.area} onChange={(e) => setForm({ ...form, area: e.target.value })}>
            {AREAS.map((a) => <option key={a} value={a}>{a}</option>)}
          </select>
          <select style={styles.select} value={form.experience_level} onChange={(e) => setForm({ ...form, experience_level: e.target.value })}>
            {LEVELS.map((l) => <option key={l} value={l}>{l}</option>)}
          </select>
          <select style={styles.select} value={form.language} onChange={(e) => setForm({ ...form, language: e.target.value })}>
            <option value="tr">Türkçe</option>
            <option value="en">İngilizce</option>
          </select>
          <select style={styles.select} value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
            <option value="employee">Çalışan</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <div style={styles.noteSection}>
          <p style={{ fontWeight: 600, marginBottom: 8 }}>Profil Notları</p>
          <div style={styles.row}>
            <input style={styles.input} placeholder="Anahtar (ör: docker)" value={noteInput.key} onChange={(e) => setNoteInput({ ...noteInput, key: e.target.value })} />
            <input style={styles.input} placeholder="Not (ör: Docker bilmiyor)" value={noteInput.value} onChange={(e) => setNoteInput({ ...noteInput, value: e.target.value })} />
            <button style={styles.addBtn} onClick={addNote}>Ekle</button>
          </div>
          {form.notes.map((n, i) => (
            <div key={i} style={styles.noteTag}>
              <strong>{n.key}</strong>: {n.value}
              <button style={styles.removeBtn} onClick={() => removeNote(i)}>×</button>
            </div>
          ))}
        </div>

        {message && <p style={{ marginBottom: 12, color: message.startsWith("✅") ? "#10b981" : "#dc2626" }}>{message}</p>}
        <button style={styles.createBtn} onClick={handleCreate} disabled={loading}>
          {loading ? "Oluşturuluyor..." : "Kullanıcı Oluştur"}
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: { padding: 24, maxWidth: 800, margin: "0 auto" },
  title: { fontSize: 24, fontWeight: 700, marginBottom: 24 },
  section: { background: "#fff", borderRadius: 12, padding: 24, border: "1px solid #e5e7eb" },
  sectionTitle: { fontWeight: 700, marginBottom: 16, fontSize: 16 },
  grid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 12 },
  row: { display: "flex", gap: 10, marginBottom: 12, flexWrap: "wrap" },
  input: { flex: 1, padding: "10px 12px", border: "1px solid #ddd", borderRadius: 8, fontSize: 14, minWidth: 120 },
  select: { flex: 1, padding: "10px 12px", border: "1px solid #ddd", borderRadius: 8, fontSize: 14, minWidth: 100 },
  noteSection: { marginBottom: 16 },
  noteTag: { display: "inline-flex", alignItems: "center", gap: 6, background: "#f3f4f6", padding: "4px 10px", borderRadius: 20, marginRight: 8, marginBottom: 6, fontSize: 13 },
  addBtn: { padding: "10px 16px", background: "#4f46e5", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer" },
  removeBtn: { background: "none", border: "none", cursor: "pointer", color: "#dc2626", fontWeight: 700 },
  createBtn: { padding: "12px 24px", background: "#10b981", color: "#fff", border: "none", borderRadius: 8, fontSize: 15, fontWeight: 700, cursor: "pointer" },
};
