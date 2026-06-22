"""
İçerik bilgi endpoint'leri (alan listesi vb.)
"""
from fastapi import APIRouter, Depends
from app.models.user import UserProfile
from app.core.auth import get_current_user
from app.content.loader import list_available_areas

router = APIRouter(prefix="/content", tags=["content"])


@router.get("/areas")
def available_areas(current_user: UserProfile = Depends(get_current_user)):
    return list_available_areas(current_user.language)
