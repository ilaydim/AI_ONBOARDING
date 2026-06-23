import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/api";
import { saveAuth } from "../utils/auth";
import { useLanguage } from "../contexts/LanguageContext";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { lang, setLang, t } = useLanguage();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await login(username, password);
      saveAuth(data.access_token, data.user);
      if (data.user.language) setLang(data.user.language);
      navigate(data.user.role === "admin" ? "/admin" : "/onboarding");
    } catch (err) {
      setError(err.response?.data?.detail || t("login.error"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.topRow}>
          <h1 style={styles.logo}>🚀 OnboardAI</h1>
          <button style={styles.langBtn} onClick={() => setLang(lang === "en" ? "tr" : "en")}>
            {lang === "en" ? "🇹🇷 TR" : "🇬🇧 EN"}
          </button>
        </div>
        <p style={styles.subtitle}>{t("login.subtitle")}</p>
        <form onSubmit={handleSubmit}>
          <input
            style={styles.input}
            placeholder={t("login.username")}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            style={styles.input}
            type="password"
            placeholder={t("login.password")}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p style={styles.error}>{error}</p>}
          <button style={styles.btn} type="submit" disabled={loading}>
            {loading ? t("login.submitting") : t("login.submit")}
          </button>
        </form>
        <p style={styles.notice}>{t("login.notice")}</p>
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "#f0f4ff" },
  card: { background: "#fff", padding: 40, borderRadius: 16, boxShadow: "0 4px 24px rgba(0,0,0,0.08)", width: 360 },
  topRow: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 },
  logo: { fontSize: 28, margin: 0 },
  langBtn: { padding: "4px 10px", background: "#f3f4f6", border: "1px solid #ddd", borderRadius: 6, cursor: "pointer", fontSize: 12, fontWeight: 600 },
  subtitle: { color: "#666", marginBottom: 24, textAlign: "center" },
  input: { width: "100%", padding: "12px 14px", marginBottom: 12, border: "1px solid #ddd", borderRadius: 8, fontSize: 14, outline: "none", boxSizing: "border-box" },
  btn: { width: "100%", padding: "13px", background: "#4f46e5", color: "#fff", border: "none", borderRadius: 8, fontSize: 15, cursor: "pointer", fontWeight: 600 },
  error: { color: "#dc2626", marginBottom: 12, fontSize: 13 },
  notice: { marginTop: 20, fontSize: 12, color: "#9ca3af", textAlign: "center", lineHeight: 1.5 },
};
