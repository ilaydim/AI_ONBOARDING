"""
Kullanıcı başına LLM API rate limiting — SRS §7.2 (NFR-2.9)
In-memory; Faz 2'de Redis ile değiştirilecek.
"""
from collections import defaultdict, deque
from datetime import datetime, timedelta
from fastapi import HTTPException

# Kullanıcı başına 1 dakikada max LLM çağrısı
_WINDOW_SECONDS = 60
_MAX_CALLS = 15

# user_id → deque of timestamps
_call_log: dict[str, deque] = defaultdict(deque)


def check_llm_rate_limit(user_id: str):
    """Limiti aştıysa 429 fırlatır."""
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=_WINDOW_SECONDS)
    q = _call_log[user_id]

    # Eski kayıtları temizle
    while q and q[0] < cutoff:
        q.popleft()

    if len(q) >= _MAX_CALLS:
        raise HTTPException(
            status_code=429,
            detail=f"Çok fazla istek gönderdin. Lütfen {_WINDOW_SECONDS} saniye bekle.",
        )

    q.append(now)
