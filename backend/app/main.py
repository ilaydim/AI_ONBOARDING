"""
OnboardAI — FastAPI uygulaması
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, chat, tasks, proficiency, progress, content

app = FastAPI(
    title="OnboardAI API",
    description="AI destekli çalışan onboarding sistemi — ICERI2026 PoC",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(tasks.router)
app.include_router(proficiency.router)
app.include_router(progress.router)
app.include_router(content.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "OnboardAI"}
