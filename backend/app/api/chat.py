"""
Konuşma tabanlı etkileşim — SRS §4.2
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.models.user import UserProfile
from app.models.session import Message
from app.core.auth import get_current_user
from app.content.loader import build_context
from app.content.progress_store import increment_question_count, record_gap, get_task_progress, touch_task_activity, has_gap
from app.content.task_parser import parse_tasks
from app.core.settings import get_config
from app.llm.factory import get_llm_adapter
from app.llm.prompt_builder import build_system_prompt
from app.core.logger import log_llm_call
from app.core.rate_limit import check_llm_rate_limit
from app.core.sanitize import sanitize_user_input
from app.llm.history import trim_history
from datetime import datetime
import time
import json

router = APIRouter(prefix="/chat", tags=["chat"])

# In-memory konuşma geçmişi (Faz 1) — key: user_id
_sessions: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    message: str
    task_id: str | None = None



class ChatResponse(BaseModel):
    reply: str
    timestamp: str
    gap_warning: bool = False
    time_warning: bool = False  # FR-4.6: görev tahmini sürenin çarpanını aştı


@router.post("", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    current_user: UserProfile = Depends(get_current_user),
):
    uid = current_user.id
    check_llm_rate_limit(uid)
    message = sanitize_user_input(req.message)
    if not message:
        raise HTTPException(status_code=400, detail="Empty message")
    adapter = get_llm_adapter()
    history = _sessions[uid] = trim_history(_sessions.get(uid, []), adapter)

    context = build_context(
        area=current_user.area,
        query=message,
        language=current_user.language,
    )

    system_prompt = build_system_prompt(
        profile=current_user.model_dump(),
        context=context,
        language=current_user.language,
    )

    t0 = time.time()
    try:
        reply = adapter.send_message(system_prompt, history, message)
        log_llm_call(uid, elapsed_ms=(time.time() - t0) * 1000, success=True)
    except Exception as e:
        log_llm_call(uid, elapsed_ms=(time.time() - t0) * 1000, success=False, error=type(e).__name__)
        raise HTTPException(status_code=503, detail="LLM servisi şu an erişilemiyor. Lütfen biraz sonra tekrar dene.")

    # Geçmişi güncelle
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})

    # Gap detection — FR-4.5: eşik aşılınca bir kez boşluk kaydet
    gap_warning = False
    time_warning = False
    if req.task_id:
        gap_cfg = get_config()["gap_detection"]
        threshold = gap_cfg["question_threshold"]
        increment_question_count(uid, req.task_id)
        progress = get_task_progress(uid)
        task_p = progress.get(req.task_id)
        question_count = task_p.question_count if task_p else 0
        if question_count == threshold:
            # Sadece eşiğe ilk ulaşıldığında kaydet, her soruda değil
            record_gap(uid, req.task_id, "question_count")
        gap_warning = question_count >= threshold

        # FR-4.5/4.6: aktif süre tahmini sürenin time_multiplier katını aşarsa boşluk sinyali
        task = next((t for t in parse_tasks(current_user.area, current_user.language) if t.id == req.task_id), None)
        active_minutes = touch_task_activity(uid, req.task_id)
        if task and active_minutes > task.estimated_hours * 60 * gap_cfg["time_multiplier"]:
            time_warning = True
            if not has_gap(uid, req.task_id, "time_exceeded"):
                record_gap(uid, req.task_id, "time_exceeded")

    now = datetime.utcnow().isoformat()
    return ChatResponse(reply=reply, timestamp=now, gap_warning=gap_warning, time_warning=time_warning)


@router.delete("/history")
def clear_history(current_user: UserProfile = Depends(get_current_user)):
    _sessions.pop(current_user.id, None)
    return {"message": "Konuşma geçmişi temizlendi"}


@router.get("/history")
def get_history(current_user: UserProfile = Depends(get_current_user)):
    return _sessions.get(current_user.id, [])
