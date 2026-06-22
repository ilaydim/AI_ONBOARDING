"""
Konuşma tabanlı etkileşim — SRS §4.2
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.models.user import UserProfile
from app.models.session import Message
from app.core.auth import get_current_user
from app.content.loader import build_context
from app.content.progress_store import increment_question_count, record_gap
from app.llm.factory import get_llm_adapter
from app.llm.prompt_builder import build_system_prompt
from datetime import datetime
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


@router.post("", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    current_user: UserProfile = Depends(get_current_user),
):
    uid = current_user.id
    history = _sessions.setdefault(uid, [])

    # Context: sorguya göre ilgili chunk'lar
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
    try:
        reply = adapter.send_message(system_prompt, history, req.message)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM servisi şu an erişilemiyor: {str(e)}")

    # Geçmişi güncelle
    history.append({"role": "user", "content": req.message})
    history.append({"role": "assistant", "content": reply})

    # Gap detection: görev bazlı soru sayısını artır
    if req.task_id:
        increment_question_count(uid, req.task_id)

    now = datetime.utcnow().isoformat()
    return ChatResponse(reply=reply, timestamp=now)


@router.delete("/history")
def clear_history(current_user: UserProfile = Depends(get_current_user)):
    _sessions.pop(current_user.id, None)
    return {"message": "Konuşma geçmişi temizlendi"}


@router.get("/history")
def get_history(current_user: UserProfile = Depends(get_current_user)):
    return _sessions.get(current_user.id, [])
