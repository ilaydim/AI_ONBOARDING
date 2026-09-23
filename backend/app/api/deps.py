"""
Ortak FastAPI bağımlılıkları.
"""
from fastapi import Depends, HTTPException
from app.core.auth import get_current_user
from app.core.logger import log_content_issue
from app.content.loader import validate_area
from app.models.user import UserProfile


def area_ready(current_user: UserProfile = Depends(get_current_user)) -> UserProfile:
    """
    CM-1.5 / NFR-5.3: çalışanın alanının içeriği eksik/hatalıysa yalnızca o alan devre dışı kalır,
    diğer alanlar çalışmaya devam eder. Kullanıcıya teknik detay vermeden ne yapması gerektiği söylenir.
    """
    problems = validate_area(current_user.area, current_user.language)["errors"]
    if problems:
        log_content_issue(current_user.area, current_user.language, problems)
        raise HTTPException(
            status_code=503,
            detail="Content for your area is temporarily unavailable. Please contact your administrator.",
        )
    return current_user
