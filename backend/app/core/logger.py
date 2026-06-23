"""
Yapılandırılmış JSON loglama — SRS §7.7 (NFR-7.1, NFR-7.2, NFR-7.3)
Her satır bağımsız bir JSON nesnesidir (JSON Lines formatı).
Log hassas kullanıcı verisi içermez (NFR-7.4).
"""
import json
import os
from datetime import datetime

_LOG_FILE = os.path.join(os.path.dirname(__file__), "../../data/app.log")


def _write(entry: dict):
    os.makedirs(os.path.dirname(_LOG_FILE), exist_ok=True)
    with open(_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def log_llm_call(user_id: str, elapsed_ms: float, success: bool, error: str | None = None):
    """NFR-7.1: LLM API çağrısı logu."""
    _write({
        "ts": datetime.utcnow().isoformat(),
        "event": "llm_call",
        "user_id": user_id,
        "elapsed_ms": round(elapsed_ms, 1),
        "success": success,
        "error": error,
    })


def log_auth_failure(username: str, reason: str):
    """NFR-7.2: Başarısız kimlik doğrulama."""
    _write({
        "ts": datetime.utcnow().isoformat(),
        "event": "auth_failure",
        "username": username,
        "reason": reason,
    })


def log_task_event(user_id: str, task_id: str, event: str, passed: bool | None = None):
    """NFR-7.3: Görev tamamlama ve yeterlilik testi eventleri."""
    _write({
        "ts": datetime.utcnow().isoformat(),
        "event": event,           # "task_complete" | "task_skip" | "proficiency_submit"
        "user_id": user_id,
        "task_id": task_id,
        "passed": passed,
    })
