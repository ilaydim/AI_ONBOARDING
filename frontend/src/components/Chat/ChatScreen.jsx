import React, { useState, useRef, useEffect } from "react";
import { sendMessage } from "../../services/api";

export default function ChatScreen({ user, currentTaskId }) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: `Merhaba ${user.first_name}! Ben OnboardAI asistanın. ${user.area} alanındaki onboarding sürecinde sana yardımcı olacağım. Sormak istediğin bir şey var mı?`,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);
    try {
      const data = await sendMessage(userMsg, currentTaskId);
      setMessages((prev) => [...prev, { role: "assistant", content: data.reply }]);
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "⚠️ Bağlantı hatası. Lütfen tekrar dene." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.messages}>
        {messages.map((m, i) => (
          <div key={i} style={{ ...styles.bubble, ...(m.role === "user" ? styles.userBubble : styles.aiBubble) }}>
            <span style={styles.roleLabel}>{m.role === "user" ? "Sen" : "🤖 Asistan"}</span>
            <p style={{ whiteSpace: "pre-wrap" }}>{m.content}</p>
          </div>
        ))}
        {loading && (
          <div style={{ ...styles.bubble, ...styles.aiBubble }}>
            <span style={styles.roleLabel}>🤖 Asistan</span>
            <p style={{ color: "#999" }}>Yanıt hazırlanıyor...</p>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      <div style={styles.inputRow}>
        <input
          style={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
          placeholder="Bir soru sor veya görev hakkında yardım al..."
        />
        <button style={styles.sendBtn} onClick={handleSend} disabled={loading}>
          Gönder
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: { display: "flex", flexDirection: "column", height: "100%", background: "#fff", borderRadius: 12, overflow: "hidden", border: "1px solid #e5e7eb" },
  messages: { flex: 1, overflowY: "auto", padding: 16, display: "flex", flexDirection: "column", gap: 12 },
  bubble: { padding: "12px 16px", borderRadius: 12, maxWidth: "80%", lineHeight: 1.6 },
  userBubble: { background: "#4f46e5", color: "#fff", alignSelf: "flex-end" },
  aiBubble: { background: "#f3f4f6", color: "#111", alignSelf: "flex-start" },
  roleLabel: { fontSize: 11, fontWeight: 700, opacity: 0.7, display: "block", marginBottom: 4 },
  inputRow: { display: "flex", gap: 8, padding: 12, borderTop: "1px solid #e5e7eb" },
  input: { flex: 1, padding: "10px 14px", border: "1px solid #ddd", borderRadius: 8, fontSize: 14, outline: "none" },
  sendBtn: { padding: "10px 20px", background: "#4f46e5", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontWeight: 600 },
};
