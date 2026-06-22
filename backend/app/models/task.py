from pydantic import BaseModel
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    skipped = "skipped"


class Task(BaseModel):
    id: str                                    # ör. "backend-001"
    title: str
    levels: list[str]                          # ["junior", "mid", "senior"]
    dependency: Optional[str] = None           # ör. "backend-001"
    expected_output: str
    completion_criteria: str
    estimated_hours: float
    skippable: bool = True


class TaskProgress(BaseModel):
    task_id: str
    status: TaskStatus = TaskStatus.pending
    elapsed_minutes: float = 0.0
    question_count: int = 0
    attempts: int = 0


class LearningPath(BaseModel):
    user_id: str
    area: str
    tasks: list[Task]
    progress: list[TaskProgress] = []


class TaskCompletionRequest(BaseModel):
    task_id: str
    user_output: str                           # çalışanın yazdığı özet/çıktı


class TaskCompletionResult(BaseModel):
    task_id: str
    passed: bool
    feedback: str
    next_task_id: Optional[str] = None
