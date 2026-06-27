"""
İlerleme verisini JSON dosyasına yazar/okur — SRS §4.4, §7.5 (NFR-5.2)
Faz 2'de veritabanına taşınacak.
"""
import json
import os
from app.models.task import TaskProgress, TaskStatus, LearningPath
from app.models.session import GapRecord

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")


def _progress_file(user_id: str) -> str:
    return os.path.join(DATA_DIR, f"progress_{user_id}.json")


def _load(user_id: str) -> dict:
    fp = _progress_file(user_id)
    if not os.path.exists(fp):
        return {"tasks": {}, "gaps": [], "session_count": 0}
    with open(fp) as f:
        return json.load(f)


def _save(user_id: str, data: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(_progress_file(user_id), "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ─── Task progress ────────────────────────────────────────────────────────────

def get_task_progress(user_id: str) -> dict[str, TaskProgress]:
    data = _load(user_id)
    return {k: TaskProgress(**v) for k, v in data.get("tasks", {}).items()}


def save_task_progress(user_id: str, task_id: str, progress: TaskProgress):
    data = _load(user_id)
    data.setdefault("tasks", {})[task_id] = progress.model_dump()
    _save(user_id, data)


def mark_task_completed(user_id: str, task_id: str, elapsed_minutes: float = 0.0):
    data = _load(user_id)
    entry = data.setdefault("tasks", {}).setdefault(task_id, {})
    entry["status"] = TaskStatus.completed
    entry["elapsed_minutes"] = round(entry.get("elapsed_minutes", 0) + elapsed_minutes, 1)
    _save(user_id, data)


def mark_task_skipped(user_id: str, task_id: str, elapsed_minutes: float = 0.0):
    data = _load(user_id)
    entry = data.setdefault("tasks", {}).setdefault(task_id, {})
    entry["status"] = TaskStatus.skipped
    entry["elapsed_minutes"] = round(entry.get("elapsed_minutes", 0) + elapsed_minutes, 1)
    _save(user_id, data)


def resume_task(user_id: str, task_id: str):
    data = _load(user_id)
    if task_id in data.get("tasks", {}):
        data["tasks"][task_id]["status"] = TaskStatus.pending
        _save(user_id, data)


def increment_question_count(user_id: str, task_id: str):
    data = _load(user_id)
    task = data.setdefault("tasks", {}).setdefault(task_id, {"question_count": 0})
    task["question_count"] = task.get("question_count", 0) + 1
    _save(user_id, data)


# ─── Gap detection — SRS §4.4 ────────────────────────────────────────────────

def record_gap(user_id: str, topic: str, signal: str):
    data = _load(user_id)
    gaps = data.setdefault("gaps", [])
    for g in gaps:
        if g["topic"] == topic:
            g["count"] += 1
            _save(user_id, data)
            return
    gaps.append({"topic": topic, "signal": signal, "count": 1})
    _save(user_id, data)


def get_gaps(user_id: str) -> list[GapRecord]:
    data = _load(user_id)
    return [GapRecord(**g) for g in data.get("gaps", [])]


# ─── Proficiency test takibi — SRS §FR-4.11 ─────────────────────────────────

def record_proficiency_attempt(user_id: str, note_key: str, passed: bool, score: float):
    data = _load(user_id)
    tests = data.setdefault("proficiency_tests", {})
    entry = tests.setdefault(note_key, {"attempts": 0, "failed_attempts": 0, "passed": False})
    entry["attempts"] += 1
    if passed:
        entry["passed"] = True
    else:
        entry["failed_attempts"] += 1
    entry["last_score"] = round(score, 1)
    _save(user_id, data)


def get_proficiency_summary(user_id: str) -> list:
    data = _load(user_id)
    tests = data.get("proficiency_tests", {})
    return [
        {"note_key": k, **v}
        for k, v in tests.items()
    ]


# ─── Summary ─────────────────────────────────────────────────────────────────

def get_completion_stats(user_id: str) -> dict:
    data = _load(user_id)
    tasks = data.get("tasks", {})
    completed = sum(1 for t in tasks.values() if t.get("status") == TaskStatus.completed)
    skipped = sum(1 for t in tasks.values() if t.get("status") == TaskStatus.skipped)
    total = len(tasks)
    pct = round((completed / total * 100), 1) if total else 0
    return {
        "total": total,
        "completed": completed,
        "skipped": skipped,
        "pending": total - completed - skipped,
        "completion_percentage": pct,
        "gaps": get_gaps(user_id),
    }
