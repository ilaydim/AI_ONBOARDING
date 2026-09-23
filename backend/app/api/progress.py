"""
İlerleme Takibi ve Yönetici Raporu — SRS §4.4
"""
from fastapi import APIRouter, Depends
from app.models.user import UserProfile
from app.core.auth import get_current_user, require_admin, _load_users
from app.content.progress_store import get_gaps, get_proficiency_summary, get_task_progress
from app.api.tasks import personalized_path, path_stats
from app.models.task import TaskStatus
from app.llm.factory import get_llm_adapter
from app.llm.prompt_builder import get_session_summary_prompt
from app.api.chat import _sessions

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/me")
def my_progress(current_user: UserProfile = Depends(get_current_user)):
    path = personalized_path(current_user.area, current_user.language, current_user.experience_level,
                             [n.model_dump() for n in current_user.notes])
    return {**path_stats(path, get_task_progress(current_user.id)), "gaps": get_gaps(current_user.id)}


@router.get("/me/gaps")
def my_gaps(current_user: UserProfile = Depends(get_current_user)):
    return get_gaps(current_user.id)


@router.post("/me/session-summary")
def generate_session_summary(current_user: UserProfile = Depends(get_current_user)):
    """Oturum sonunda LLM ile özet üret — SRS §FR-4.4"""
    history = _sessions.get(current_user.id, [])
    lang = current_user.language
    if not history:
        msg = "Bu oturumda henüz konuşma yapılmamış." if lang == "tr" else "No conversation in this session yet."
        return {"summary": msg}

    # Gerçek ilerleme istatistiklerini al
    path = personalized_path(current_user.area, current_user.language, current_user.experience_level,
                             [n.model_dump() for n in current_user.notes])
    st = path_stats(path, get_task_progress(current_user.id))
    completed, skipped, total, pending = st["completed"], st["skipped"], st["total"], st["pending"]

    user_label = "Çalışan" if lang == "tr" else "Employee"
    ai_label = "Asistan" if lang == "tr" else "Assistant"
    conversation_text = "\n".join(
        f"{user_label if m['role'] == 'user' else ai_label}: {m['content']}"
        for m in history[-30:]
    )

    prompt = get_session_summary_prompt(lang).format(
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        area=current_user.area,
        completed=completed,
        skipped=skipped,
        pending=pending,
        total=total,
        conversation=conversation_text,
    )

    adapter = get_llm_adapter()
    sys = "Sen bir eğitim koordinatörüsün." if lang == "tr" else "You are a training coordinator."
    try:
        summary = adapter.send_message(
            system_prompt=sys,
            conversation_history=[],
            user_message=prompt,
        )
    except Exception as e:
        return {"summary": "Özet şu an üretilemedi. Lütfen daha sonra tekrar dene."}

    return {"summary": summary}


# ─── Admin endpoints ──────────────────────────────────────────────────────────

@router.get("/admin/{user_id}")
def admin_user_progress(
    user_id: str,
    _admin: UserProfile = Depends(require_admin),
):
    """Yönetici: belirli bir çalışanın ilerleme raporu — SRS §FR-4.9, FR-4.10, FR-4.11"""
    users = _load_users()
    u = users.get(user_id, {})
    area = u.get("area", "")
    level = u.get("experience_level", "")
    lang = u.get("language", "tr")

    # Çalışanın kendi ekranıyla aynı hesap (kişiselleştirilmiş yol)
    path = personalized_path(area, lang, level, u.get("notes", [])) if area and level else []
    stats = path_stats(path, get_task_progress(user_id))

    gaps = get_gaps(user_id)
    proficiency = get_proficiency_summary(user_id)
    return {"user_id": user_id, "stats": stats, "gaps": gaps, "proficiency_tests": proficiency}
