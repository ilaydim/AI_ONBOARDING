import React, { useState, useRef, useEffect } from "react";
import { sendMessage, completeTask } from "../../services/api";
import { useLanguage } from "../../contexts/LanguageContext";

export default function ChatScreen({ user, currentTaskId, currentTask, onTaskCompleted }) {
  const { t } = useLanguage();

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: t("chat.welcome", { name: user.first_name, area: user.area }),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showCompleteForm, setShowCompleteForm] = useState(false);
  const [completionOutput, setCompletionOutput] = useState("");
  const [completing, setCompleting] = useState(false);
  const [pendingHelp, setPendingHelp] = useState(null);
  const bottomRef = useRef(null);
  const taskStartRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    setShowCompleteForm(false);
    setCompletionOutput("");
    taskStartRef.current = currentTaskId ? Date.now() : null;
  }, [currentTaskId]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);
    try {
      const data = await sendMessage(userMsg, currentTaskId);
      setMessages((prev) => {
        const next = [...prev, { role: "assistant", content: data.reply }];
        if (data.gap_warning) next.push({ role: "system", content: t("chat.gapWarning") });
        return next;
      });
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: t("chat.connectionError") }]);
    } finally {
      setLoading(false);
    }
  };

  const handleComplete = async () => {
    if (!completionOutput.trim() || completing) return;
    setCompleting(true);
    setShowCompleteForm(false);
    const elapsedMinutes = taskStartRef.current
      ? Math.round((Date.now() - taskStartRef.current) / 60000 * 10) / 10
      : 0;
    setMessages((prev) => [
      ...prev,
      { role: "user", content: t("chat.taskOutput", { output: completionOutput }) },
    ]);
    try {
      const result = await completeTask(currentTaskId, completionOutput, elapsedMinutes);
      if (result.passed) {
        const key = result.next_task_id ? "chat.passed" : "chat.passedAll";
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: t(key, { feedback: result.feedback }) },
        ]);
        setCompletionOutput("");
        onTaskCompleted?.();
      } else {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: t("chat.failed", { feedback: result.feedback }) },
        ]);
        setPendingHelp(
          t("chat.pendingHelpMsg", {
            title: currentTask?.title || "this task",
            criteria: currentTask?.completion_criteria || "not specified",
          })
        );
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: t("chat.evaluationError") },
      ]);
    } finally {
      setCompleting(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.messages}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              ...styles.bubble,
              ...(m.role === "user" ? styles.userBubble : m.role === "system" ? styles.systemBubble : styles.aiBubble),
            }}
          >
            {m.role !== "system" && (
              <span style={styles.roleLabel}>
                {m.role === "user" ? t("chat.you") : t("chat.assistant")}
              </span>
            )}
            <p style={{ whiteSpace: "pre-wrap", margin: 0 }}>{m.content}</p>
          </div>
        ))}
        {(loading || completing) && (
          <div style={{ ...styles.bubble, ...styles.aiBubble }}>
            <span style={styles.roleLabel}>{t("chat.assistant")}</span>
            <p style={{ color: "#999", margin: 0 }}>
              {completing ? t("chat.evaluating") : t("chat.thinking")}
            </p>
          </div>
        )}
        {pendingHelp && (
          <div style={styles.helpSuggestion}>
            <span style={styles.helpIcon}>💡</span>
            <span style={styles.helpText}>{t("chat.helpPrompt")}</span>
            <button
              style={styles.helpBtn}
              onClick={() => { setInput(pendingHelp); setPendingHelp(null); }}
            >
              {t("chat.getHelp")}
            </button>
            <button style={styles.helpDismiss} onClick={() => setPendingHelp(null)}>×</button>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {currentTaskId && (
        <div style={styles.completeArea}>
          {!showCompleteForm ? (
            <button
              style={styles.completeToggleBtn}
              onClick={() => setShowCompleteForm(true)}
              disabled={completing || loading}
            >
              {t("chat.completeTask")}
            </button>
          ) : (
            <div style={styles.completeForm}>
              <p style={styles.completeLabel}>
                {currentTask?.completion_criteria
                  ? t("chat.criterion", { criteria: currentTask.completion_criteria })
                  : t("chat.criterionDefault")}
              </p>
              <textarea
                style={styles.textarea}
                rows={4}
                placeholder={t("chat.placeholder")}
                value={completionOutput}
                onChange={(e) => setCompletionOutput(e.target.value)}
              />
              <div style={styles.completeActions}>
                <button
                  style={styles.cancelBtn}
                  onClick={() => { setShowCompleteForm(false); setCompletionOutput(""); }}
                >
                  {t("chat.cancel")}
                </button>
                <button
                  style={{ ...styles.submitBtn, opacity: !completionOutput.trim() ? 0.5 : 1 }}
                  onClick={handleComplete}
                  disabled={!completionOutput.trim() || completing}
                >
                  {t("chat.submitReview")}
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      <div style={styles.inputRow}>
        <input
          style={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
          placeholder={t("chat.inputPlaceholder")}
          disabled={loading || completing}
        />
        <button style={styles.sendBtn} onClick={handleSend} disabled={loading || completing}>
          {t("chat.send")}
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
  systemBubble: { background: "#fef9c3", color: "#713f12", alignSelf: "center", maxWidth: "90%", border: "1px solid #fde68a", fontSize: 13 },
  roleLabel: { fontSize: 11, fontWeight: 700, opacity: 0.7, display: "block", marginBottom: 4 },
  completeArea: { padding: "10px 12px", borderTop: "1px solid #e5e7eb", background: "#f0fdf4" },
  completeToggleBtn: { padding: "8px 18px", background: "#10b981", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontWeight: 700, fontSize: 14 },
  completeForm: { display: "flex", flexDirection: "column", gap: 8 },
  completeLabel: { fontSize: 12, color: "#374151", fontWeight: 600, margin: 0 },
  textarea: { padding: "10px 12px", border: "1px solid #d1fae5", borderRadius: 8, fontSize: 14, resize: "vertical", fontFamily: "inherit", outline: "none" },
  completeActions: { display: "flex", gap: 8, justifyContent: "flex-end" },
  cancelBtn: { padding: "8px 14px", background: "#f3f4f6", color: "#374151", border: "1px solid #d1d5db", borderRadius: 8, cursor: "pointer", fontSize: 13 },
  submitBtn: { padding: "8px 18px", background: "#10b981", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontWeight: 700, fontSize: 13 },
  helpSuggestion: { display: "flex", alignItems: "center", gap: 8, padding: "10px 14px", background: "#fffbeb", border: "1px solid #fde68a", borderRadius: 10, margin: "4px 0" },
  helpIcon: { fontSize: 18, flexShrink: 0 },
  helpText: { flex: 1, fontSize: 13, color: "#92400e" },
  helpBtn: { padding: "6px 14px", background: "#f59e0b", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer", fontSize: 12, fontWeight: 700, flexShrink: 0 },
  helpDismiss: { background: "none", border: "none", cursor: "pointer", color: "#9ca3af", fontSize: 16, flexShrink: 0 },
  inputRow: { display: "flex", gap: 8, padding: 12, borderTop: "1px solid #e5e7eb" },
  input: { flex: 1, padding: "10px 14px", border: "1px solid #ddd", borderRadius: 8, fontSize: 14, outline: "none" },
  sendBtn: { padding: "10px 20px", background: "#4f46e5", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontWeight: 600 },
};
