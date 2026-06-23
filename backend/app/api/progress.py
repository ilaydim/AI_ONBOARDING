"""
İlerleme Takibi ve Yönetici Raporu — SRS §4.4
"""
from fastapi import APIRouter, Depends
from app.models.user import UserProfile
from app.core.auth import get_current_user, require_admin
from app.content.progress_store import get_completion_stats, get_gaps, get_proficiency_summary
from app.llm.factory import get_llm_adapter
from app.llm.prompt_builder import SESSION_SUMMARY_PROMPT_TR
from app.api.chat import _sessions

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/me")
def my_progress(current_user: UserProfile = Depends(get_current_user)):
    return get_completion_stats(current_user.id)


@router.get("/me/gaps")
def my_gaps(current_user: UserProfile = Depends(get_current_user)):
    return get_gaps(current_user.id)


@router.post("/me/session-summary")
def generate_session_summary(current_user: UserProfile = Depends(get_current_user)):
    """Oturum sonunda LLM ile özet üret — SRS §FR-4.4"""
    history = _sessions.get(current_user.id, [])
    if not history:
        return {"summary": "Bu oturumda henüz konuşma yapılmamış."}

    conversation_text = "\n".join(
        f"{'Çalışan' if m['role'] == 'user' else 'Asistan'}: {m['content']}"
        for m in history[-20:]  # Son 20 mesaj
    )

    prompt = SESSION_SUMMARY_PROMPT_TR.format(
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        area=current_user.area,
        conversation=conversation_text,
    )

    adapter = get_llm_adapter()
    try:
        summary = adapter.send_message(
            system_prompt="Sen bir eğitim koordinatörüsün.",
            conversation_history=[],
            user_message=prompt,
        )
    except Exception as e:
        return {"summary": f"Özet üretilemedi: {str(e)}"}

    return {"summary": summary}


# ─── Admin endpoints ──────────────────────────────────────────────────────────

@router.get("/admin/{user_id}")
def admin_user_progress(
    user_id: str,
    _admin: UserProfile = Depends(require_admin),
):
    """Yönetici: belirli bir çalışanın ilerleme raporu — SRS §FR-4.9, FR-4.10, FR-4.11"""
    stats = get_completion_stats(user_id)
    gaps = get_gaps(user_id)
    proficiency = get_proficiency_summary(user_id)
    return {"user_id": user_id, "stats": stats, "gaps": gaps, "proficiency_tests": proficiency}
