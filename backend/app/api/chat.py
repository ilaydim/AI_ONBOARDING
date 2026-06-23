"""
Konuşma tabanlı etkileşim — SRS §4.2
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.models.user import UserProfile
from app.models.session import Message
from app.core.auth import get_current_user
from app.content.loader import build_context
from app.content.progress_store import increment_question_count, record_gap, get_task_progress
from app.llm.factory import get_llm_adapter
from app.llm.prompt_builder import build_system_prompt
from app.core.logger import log_llm_call
from app.core.rate_limit import check_llm_rate_limit
from datetime import datetime
import time
import json

router = APIRouter(prefix="/chat", tags=["chat"])

# In-memory konuşma geçmişi (Faz 1) — key: user_id
_sessions: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    message: str
    task_id: str | None = None


GAP_QUESTION_THRESHOLD = 3  # Aynı görevde bu kadar soru → boşluk uyarısı


class ChatResponse(BaseModel):
    reply: str
    timestamp: str
    gap_warning: bool = False


@router.post("", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    current_user: UserProfile = Depends(get_current_user),
):
    uid = current_user.id
    check_llm_rate_limit(uid)
    history = _sessions.setdefault(uid, [])

    context = build_context(
        area=current_user.area,
        query=req.message,
        language=current_user.language,
    )

    system_prompt = build_system_prompt(
        profile=current_user.model_dump(),
        context=context,
        language=current_user.language,
    )

    adapter = get_llm_adapter()
    t0 = time.time()
    try:
        reply = adapter.send_message(system_prompt, history, req.message)
        log_llm_call(uid, elapsed_ms=(time.time() - t0) * 1000, success=True)
    except Exception as e:
        log_llm_call(uid, elapsed_ms=(time.time() - t0) * 1000, success=False, error=str(e))
        raise HTTPException(status_code=503, detail=f"LLM servisi şu an erişilemiyor: {str(e)}")

    # Geçmişi güncelle
    history.append({"role": "user", "content": req.message})
    history.append({"role": "assistant", "content": reply})

    # Gap detection: görev bazlı soru sayısını artır ve eşik kontrolü yap
    gap_warning = False
    if req.task_id:
        increment_question_count(uid, req.task_id)
        progress = get_task_progress(uid)
        task_p = progress.get(req.task_id)
        question_count = task_p.question_count if task_p else 0
        if question_count >= GAP_QUESTION_THRESHOLD:
            record_gap(uid, req.task_id, "question_count")
            gap_warning = True

    now = datetime.utcnow().isoformat()
    return ChatResponse(reply=reply, timestamp=now, gap_warning=gap_warning)


@router.delete("/history")
def clear_history(current_user: UserProfile = Depends(get_current_user)):
    _sessions.pop(current_user.id, None)
    return {"message": "Konuşma geçmişi temizlendi"}


@router.get("/history")
def get_history(current_user: UserProfile = Depends(get_current_user)):
    return _sessions.get(current_user.id, [])
