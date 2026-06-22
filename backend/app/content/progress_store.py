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


def mark_task_completed(user_id: str, task_id: str):
    data = _load(user_id)
    data.setdefault("tasks", {}).setdefault(task_id, {})
    data["tasks"][task_id]["status"] = TaskStatus.completed
    _save(user_id, data)


def mark_task_skipped(user_id: str, task_id: str):
    data = _load(user_id)
    data.setdefault("tasks", {}).setdefault(task_id, {})
    data["tasks"][task_id]["status"] = TaskStatus.skipped
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
