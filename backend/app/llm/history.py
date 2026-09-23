"""
Konuşma geçmişi boyut yönetimi — SRS §5.2 (LLM-2.4)
Geçmiş sınırı aşarsa eski mesajlar LLM ile özetlenip tek mesaja indirilir;
özet başarısız olursa eski mesajlar atılır.
"""
from app.llm.adapter import LLMAdapter

MAX_HISTORY_CHARS = 12000
KEEP_RECENT = 6  # her zaman korunacak son mesaj sayısı


def _size(history: list[dict]) -> int:
    return sum(len(m["content"]) for m in history)


def trim_history(history: list[dict], adapter: LLMAdapter, max_chars: int = MAX_HISTORY_CHARS) -> list[dict]:
    if _size(history) <= max_chars or len(history) <= KEEP_RECENT:
        return history

    old, recent = history[:-KEEP_RECENT], history[-KEEP_RECENT:]
    transcript = "\n".join(f"{m['role']}: {m['content']}" for m in old)
    try:
        summary = adapter.send_message(
            system_prompt="Summarize the conversation below in under 150 words. Keep facts and open questions.",
            conversation_history=[],
            user_message=transcript[:max_chars],
        )
        return [{"role": "user", "content": f"[Earlier conversation summary] {summary}"}] + recent
    except Exception:
        return recent
