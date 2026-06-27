"""
Görev bazlı öğrenme — SRS §4.3
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.models.user import UserProfile, ExperienceLevel
from app.models.task import Task, TaskStatus, TaskCompletionRequest, TaskCompletionResult
from app.core.auth import get_current_user
from app.content.task_parser import parse_tasks
from app.content.progress_store import (
    get_task_progress, save_task_progress, mark_task_completed,
    mark_task_skipped, resume_task, get_completion_stats,
)
from app.content.loader import load_area_content
from app.llm.factory import get_llm_adapter
from app.core.logger import log_task_event
from app.llm.prompt_builder import get_evaluation_prompt
import json, re

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _filter_tasks_for_level(tasks: list[Task], level: str) -> list[Task]:
    return [t for t in tasks if level in t.levels]


def _apply_profile_notes(tasks: list[Task], notes: list, level: str) -> list[Task]:
    """
    Profil notlarına göre bazı görevleri atla.
    Basit keyword eşleştirme — Faz 1 implementasyonu.
    """
    known_topics = set()
    for note in notes:
        if note.get("verified"):
            # verified nota göre ilgili keyword'ü "biliyor" say
            known_topics.add(note.get("key", "").lower())

    result = []
    for task in tasks:
        task_key = task.id.split("-")[1] if "-" in task.id else task.id
        if task_key in known_topics and task.skippable:
            continue
        result.append(task)
    return result


@router.get("/learning-path")
def get_learning_path(current_user: UserProfile = Depends(get_current_user)):
    all_tasks = parse_tasks(current_user.area, current_user.language)
    level_tasks = _filter_tasks_for_level(all_tasks, current_user.experience_level)
    filtered = _apply_profile_notes(
        level_tasks,
        [n.model_dump() for n in current_user.notes],
        current_user.experience_level,
    )

    progress = get_task_progress(current_user.id)
    result = []
    for task in filtered:
        tp = progress.get(task.id)
        result.append({
            "task": task.model_dump(),
            "status": tp.status if tp else TaskStatus.pending,
            "question_count": tp.question_count if tp else 0,
            "elapsed_minutes": tp.elapsed_minutes if tp else 0,
        })
    return result


@router.post("/complete", response_model=TaskCompletionResult)
def complete_task(
    req: TaskCompletionRequest,
    current_user: UserProfile = Depends(get_current_user),
):
    all_tasks = parse_tasks(current_user.area, current_user.language)
    task = next((t for t in all_tasks if t.id == req.task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    area_content = load_area_content(current_user.area, current_user.language)
    eval_prompt = get_evaluation_prompt(current_user.language).format(
        task_title=task.title,
        criteria=task.completion_criteria,
        user_output=req.user_output,
    )

    adapter = get_llm_adapter()
    try:
        raw = adapter.send_message(
            system_prompt="You are a technical evaluator. Respond only in JSON format.",
            conversation_history=[],
            user_message=eval_prompt,
        )
        # JSON parse
        json_str = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_str:
            result_data = json.loads(json_str.group())
        else:
            result_data = {"passed": False, "feedback": raw}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM evaluation error: {str(e)}")

    passed = result_data.get("passed", False)
    feedback = result_data.get("feedback", "")

    if passed:
        mark_task_completed(current_user.id, req.task_id, req.elapsed_minutes)
    log_task_event(current_user.id, req.task_id, "task_complete", passed=passed)

    # Sıradaki görevi bul
    level_tasks = _filter_tasks_for_level(all_tasks, current_user.experience_level)
    progress = get_task_progress(current_user.id)
    next_task = None
    found_current = False
    for t in level_tasks:
        if found_current and progress.get(t.id) is None:
            next_task = t.id
            break
        if t.id == req.task_id:
            found_current = True

    return TaskCompletionResult(
        task_id=req.task_id,
        passed=passed,
        feedback=feedback,
        next_task_id=next_task,
    )


class SkipRequest(BaseModel):
    elapsed_minutes: float = 0.0


@router.post("/{task_id}/skip")
def skip_task(task_id: str, req: SkipRequest = SkipRequest(), current_user: UserProfile = Depends(get_current_user)):
    all_tasks = parse_tasks(current_user.area, current_user.language)
    task = next((t for t in all_tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not task.skippable:
        raise HTTPException(
            status_code=400,
            detail="This task cannot be skipped — it is required for subsequent topics."
        )
    mark_task_skipped(current_user.id, task_id, req.elapsed_minutes)
    log_task_event(current_user.id, task_id, "task_skip")
    return {"message": f"Task '{task.title}' marked as skipped"}


@router.post("/{task_id}/resume")
def resume_skipped_task(task_id: str, current_user: UserProfile = Depends(get_current_user)):
    all_tasks = parse_tasks(current_user.area, current_user.language)
    task = next((t for t in all_tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    progress = get_task_progress(current_user.id)
    tp = progress.get(task_id)
    if not tp or tp.status != "skipped":
        raise HTTPException(status_code=400, detail="Task is not skipped")
    resume_task(current_user.id, task_id)
    log_task_event(current_user.id, task_id, "task_resume")
    return {"message": f"Task '{task.title}' resumed"}


@router.get("/stats")
def get_stats(current_user: UserProfile = Depends(get_current_user)):
    return get_completion_stats(current_user.id)
