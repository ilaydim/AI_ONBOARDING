"""
OnboardAI — FastAPI uygulaması
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.content.loader import content_health
from app.core.settings import get_config
from app.core.logger import log_content_issue
from app.api import auth, chat, tasks, proficiency, progress, content

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # CM-1.4: başlangıçta içerik dizinini tara; sorunları logla, çökme (NFR-5.3)
    for lang, rep in content_health().items():
        for area, res in rep["areas"].items():
            if res["errors"] or res["warnings"]:
                log_content_issue(area, lang, res["errors"] + res["warnings"])
    yield


app = FastAPI(
    lifespan=lifespan,
    title="OnboardAI API",
    description="AI destekli çalışan onboarding sistemi — ICERI2026 PoC",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_config().get("server", {}).get("cors_origins", ["http://localhost:3000"]),
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
