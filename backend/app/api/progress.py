"""
İlerleme Takibi ve Yönetici Raporu — SRS §4.4
"""
from fastapi import APIRouter, Depends
from app.models.user import UserProfile
from app.core.auth import get_current_user, require_admin, _load_users
from app.content.progress_store import get_completion_stats, get_gaps, get_proficiency_summary, get_task_progress
from app.content.task_parser import parse_tasks
from app.models.task import TaskStatus
from app.llm.factory import get_llm_adapter
from app.llm.prompt_builder import get_session_summary_prompt
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
    lang = current_user.language
    if not history:
        msg = "Bu oturumda henüz konuşma yapılmamış." if lang == "tr" else "No conversation in this session yet."
        return {"summary": msg}

    # Gerçek ilerleme istatistiklerini al
    all_tasks = parse_tasks(current_user.area, current_user.language)
    level_tasks = [t for t in all_tasks if current_user.experience_level in t.levels]
    progress_map = get_task_progress(current_user.id)
    completed = sum(1 for t in level_tasks if progress_map.get(t.id) and progress_map[t.id].status == TaskStatus.completed)
    skipped = sum(1 for t in level_tasks if progress_map.get(t.id) and progress_map[t.id].status == TaskStatus.skipped)
    total = len(level_tasks)
    pending = total - completed - skipped

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
        return {"summary": f"Özet üretilemedi: {str(e)}"}

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

    # Real total from learning path
    progress_map = get_task_progress(user_id)
    stats = get_completion_stats(user_id)
    if area and level:
        all_tasks = parse_tasks(area, lang)
        real_tasks = [t for t in all_tasks if level in t.levels]
        notes = u.get("notes", [])
        known = {n.get("key", "").lower() for n in notes if n.get("verified")}
        real_tasks = [t for t in real_tasks if not (t.id.split("-")[1] in known and t.skippable)]
        real_total = len(real_tasks)
        completed = sum(1 for t in real_tasks if progress_map.get(t.id) and progress_map[t.id].status == "completed")
        skipped = sum(1 for t in real_tasks if progress_map.get(t.id) and progress_map[t.id].status == "skipped")
        pct = round(completed / real_total * 100, 1) if real_total else 0
        stats = {
            "total": real_total,
            "completed": completed,
            "skipped": skipped,
            "pending": real_total - completed - skipped,
            "completion_percentage": pct,
        }

    gaps = get_gaps(user_id)
    proficiency = get_proficiency_summary(user_id)
    return {"user_id": user_id, "stats": stats, "gaps": gaps, "proficiency_tests": proficiency}
