from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Message(BaseModel):
    role: str          # "user" | "assistant"
    content: str
    timestamp: datetime = datetime.now()


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct_index: int


class ProficiencyTest(BaseModel):
    note_key: str
    questions: list[QuizQuestion]
    score: Optional[float] = None
    passed: Optional[bool] = None


class GapRecord(BaseModel):
    topic: str
    signal: str        # "question_count" | "time_exceeded" | "failed_test" | "out_of_scope"
    count: int = 1


class Session(BaseModel):
    user_id: str
    area: str
    language: str
    current_task_id: Optional[str] = None
    conversation_history: list[Message] = []
    gaps: list[GapRecord] = []
    session_summary: Optional[str] = None
