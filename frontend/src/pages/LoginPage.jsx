import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/api";
import { saveAuth } from "../utils/auth";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await login(username, password);
      saveAuth(data.access_token, data.user);
      navigate(data.user.role === "admin" ? "/admin" : "/onboarding");
    } catch (err) {
      setError(err.response?.data?.detail || "Giriş başarısız");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.logo}>🚀 OnboardAI</h1>
        <p style={styles.subtitle}>Hoş geldiniz. Lütfen giriş yapın.</p>
        <form onSubmit={handleSubmit}>
          <input
            style={styles.input}
            placeholder="Kullanıcı adı"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            style={styles.input}
            type="password"
            placeholder="Şifre"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p style={styles.error}>{error}</p>}
          <button style={styles.btn} type="submit" disabled={loading}>
            {loading ? "Giriş yapılıyor..." : "Giriş Yap"}
          </button>
        </form>
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "#f0f4ff" },
  card: { background: "#fff", padding: 40, borderRadius: 16, boxShadow: "0 4px 24px rgba(0,0,0,0.08)", width: 360 },
  logo: { fontSize: 28, marginBottom: 8, textAlign: "center" },
  subtitle: { color: "#666", marginBottom: 24, textAlign: "center" },
  input: { width: "100%", padding: "12px 14px", marginBottom: 12, border: "1px solid #ddd", borderRadius: 8, fontSize: 14, outline: "none" },
  btn: { width: "100%", padding: "13px", background: "#4f46e5", color: "#fff", border: "none", borderRadius: 8, fontSize: 15, cursor: "pointer", fontWeight: 600 },
  error: { color: "#dc2626", marginBottom: 12, fontSize: 13 },
};
