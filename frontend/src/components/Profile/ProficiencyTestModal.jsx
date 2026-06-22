import React, { useState, useEffect } from "react";
import { generateTest, submitTest } from "../../services/api";

export default function ProficiencyTestModal({ noteKey, onClose, onPassed }) {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    generateTest(noteKey, 4)
      .then((data) => { setQuestions(data.questions || []); })
      .catch(() => { setQuestions([]); })
      .finally(() => setLoading(false));
  }, [noteKey]);

  const handleSubmit = async () => {
    setSubmitting(true);
    const answerList = questions.map((_, i) => answers[i] ?? -1);
    try {
      const res = await submitTest(noteKey, answerList, questions);
      setResult(res);
      if (res.passed) onPassed?.();
    } catch {
      setResult({ passed: false, message: "Test gönderilemedi." });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <h2 style={styles.title}>Yeterlilik Testi: {noteKey}</h2>
        {loading && <p>Sorular hazırlanıyor...</p>}
        {!loading && questions.length === 0 && <p>Test üretilemedi.</p>}
        {!result && questions.map((q, i) => (
          <div key={i} style={styles.question}>
            <p style={styles.qText}>{i + 1}. {q.question}</p>
            {q.options.map((opt, j) => (
              <label key={j} style={styles.option}>
                <input
                  type="radio"
                  name={`q${i}`}
                  checked={answers[i] === j}
                  onChange={() => setAnswers({ ...answers, [i]: j })}
                />{" "}
                {opt}
              </label>
            ))}
          </div>
        ))}
        {result && (
          <div style={{ ...styles.result, background: result.passed ? "#f0fdf4" : "#fef2f2" }}>
            <p style={{ fontWeight: 700, color: result.passed ? "#10b981" : "#dc2626" }}>
              {result.passed ? "✅ Geçildi!" : "❌ Başarısız"}
            </p>
            <p>{result.message}</p>
          </div>
        )}
        <div style={styles.actions}>
          {!result && (
            <button style={styles.submitBtn} onClick={handleSubmit} disabled={submitting || loading}>
              {submitting ? "Gönderiliyor..." : "Testi Gönder"}
            </button>
          )}
          <button style={styles.closeBtn} onClick={onClose}>Kapat</button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  overlay: { position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 100 },
  modal: { background: "#fff", borderRadius: 16, padding: 32, maxWidth: 560, width: "90%", maxHeight: "85vh", overflowY: "auto" },
  title: { fontSize: 20, fontWeight: 700, marginBottom: 20 },
  question: { marginBottom: 20 },
  qText: { fontWeight: 600, marginBottom: 8 },
  option: { display: "block", padding: "6px 0", cursor: "pointer" },
  result: { padding: 16, borderRadius: 8, marginBottom: 16 },
  actions: { display: "flex", gap: 10, justifyContent: "flex-end" },
  submitBtn: { padding: "10px 20px", background: "#4f46e5", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontWeight: 600 },
  closeBtn: { padding: "10px 20px", background: "#f3f4f6", border: "1px solid #ddd", borderRadius: 8, cursor: "pointer" },
};
