"""
İçerik bilgi endpoint'leri (alan listesi vb.)
"""
from fastapi import APIRouter, Depends
from app.models.user import UserProfile
from app.core.auth import get_current_user, require_admin
from app.content.loader import list_available_areas, content_health

router = APIRouter(prefix="/content", tags=["content"])


@router.get("/areas")
def available_areas(current_user: UserProfile = Depends(get_current_user)):
    return list_available_areas(current_user.language)


@router.get("/health")
def health(_admin: UserProfile = Depends(require_admin)):
    """Yönetici: eksik/hatalı içerik dosyaları raporu (CM-1.5, CM-3.5)."""
    return content_health()
