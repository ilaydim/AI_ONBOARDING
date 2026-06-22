import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:8000" });

// JWT token'ı her isteğe ekle
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// 401 → login'e yönlendir
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

// ─── Auth ────────────────────────────────────────────────────────────────────
export const login = (username, password) =>
  api.post("/auth/login", { username, password }).then((r) => r.data);

export const createUser = (userData) =>
  api.post("/auth/users", userData).then((r) => r.data);

export const getMe = () => api.get("/auth/me").then((r) => r.data);

// ─── Chat ────────────────────────────────────────────────────────────────────
export const sendMessage = (message, taskId = null) =>
  api.post("/chat", { message, task_id: taskId }).then((r) => r.data);

export const getChatHistory = () =>
  api.get("/chat/history").then((r) => r.data);

export const clearHistory = () => api.delete("/chat/history");

// ─── Tasks ───────────────────────────────────────────────────────────────────
export const getLearningPath = () =>
  api.get("/tasks/learning-path").then((r) => r.data);

export const completeTask = (taskId, userOutput) =>
  api.post("/tasks/complete", { task_id: taskId, user_output: userOutput }).then((r) => r.data);

export const skipTask = (taskId) =>
  api.post(`/tasks/${taskId}/skip`).then((r) => r.data);

export const getTaskStats = () =>
  api.get("/tasks/stats").then((r) => r.data);

// ─── Proficiency ─────────────────────────────────────────────────────────────
export const generateTest = (noteKey, questionCount = 4) =>
  api.post("/proficiency/generate", { note_key: noteKey, question_count: questionCount }).then((r) => r.data);

export const submitTest = (noteKey, answers, questions) =>
  api.post("/proficiency/submit", { note_key: noteKey, answers, questions }).then((r) => r.data);

// ─── Progress ────────────────────────────────────────────────────────────────
export const getMyProgress = () =>
  api.get("/progress/me").then((r) => r.data);

export const getMyGaps = () =>
  api.get("/progress/me/gaps").then((r) => r.data);

export const getSessionSummary = () =>
  api.post("/progress/me/session-summary").then((r) => r.data);

export const getAdminProgress = (userId) =>
  api.get(`/progress/admin/${userId}`).then((r) => r.data);

export default api;
