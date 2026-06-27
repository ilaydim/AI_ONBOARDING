"""
Yeterlilik Testi — SRS §4.1 (FR-1.7 … FR-1.10)
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.models.user import UserProfile
from app.core.auth import get_current_user
from app.content.loader import load_area_content
from app.llm.factory import get_llm_adapter
from app.llm.prompt_builder import get_quiz_prompt
from app.content.progress_store import record_proficiency_attempt, record_gap
from app.core.logger import log_task_event
import json, re

router = APIRouter(prefix="/proficiency", tags=["proficiency"])


class GenerateTestRequest(BaseModel):
    note_key: str      # profil notundaki anahtar kelime, ör. "docker"
    question_count: int = 4


class SubmitTestRequest(BaseModel):
    note_key: str
    answers: list[int]          # her soru için seçilen index
    questions: list[dict]       # GenerateTest'ten gelen sorular (correct_index içeriyor)


@router.post("/generate")
def generate_test(
    req: GenerateTestRequest,
    current_user: UserProfile = Depends(get_current_user),
):
    area_content = load_area_content(current_user.area, current_user.language)
    prompt = get_quiz_prompt(current_user.language).format(
        count=req.question_count,
        topic=req.note_key,
        level=current_user.experience_level,
        context=area_content[:3000],  # token limitine karşı kıs
    )

    adapter = get_llm_adapter()
    try:
        raw = adapter.send_message(
            system_prompt="You are a technical evaluator. Respond only in JSON format.",
            conversation_history=[],
            user_message=prompt,
        )
        json_str = re.search(r'\{.*\}', raw, re.DOTALL)
        data = json.loads(json_str.group()) if json_str else {}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Test generation error: {str(e)}")

    return data


@router.post("/submit")
def submit_test(
    req: SubmitTestRequest,
    current_user: UserProfile = Depends(get_current_user),
):
    """
    Testi değerlendir. Geçme kriteri %70 (SRS Faz1).
    Geçilirse ilgili profil notunu 'verified=True' yap.
    """
    questions = req.questions
    correct = sum(
        1 for i, q in enumerate(questions)
        if i < len(req.answers) and req.answers[i] == q.get("correct_index")
    )
    score = correct / len(questions) if questions else 0
    passed = score >= 0.70

    if passed:
        # Profil notunu güncelle — users.json'dan yükle ve kaydet
        from app.core.auth import _load_users, _save_users
        users = _load_users()
        if current_user.id in users:
            notes = users[current_user.id].get("notes", [])
            for note in notes:
                if note.get("key") == req.note_key:
                    note["verified"] = True
            users[current_user.id]["notes"] = notes
            _save_users(users)

    record_proficiency_attempt(current_user.id, req.note_key, passed, score * 100)
    if not passed:
        record_gap(current_user.id, req.note_key, "proficiency_failed")
    log_task_event(current_user.id, req.note_key, "proficiency_submit", passed=passed)

    return {
        "score": round(score * 100, 1),
        "passed": passed,
        "correct": correct,
        "total": len(questions),
        "note_key": req.note_key,
        "message": (
            f"Congratulations! Your knowledge of '{req.note_key}' has been verified and removed from your learning path."
            if passed else
            f"The 70% threshold was not reached ({round(score*100,1)}%). This topic remains in your learning path."
        ),
    }
