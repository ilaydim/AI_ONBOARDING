from fastapi import APIRouter, Depends, HTTPException
from app.models.user import LoginRequest, TokenResponse, UserCreate, UserProfile
from app.core.auth import authenticate_user, create_token, create_user, require_admin, get_current_user
from app.core.logger import log_auth_failure

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    result = authenticate_user(data.username, data.password)
    if not result:
        log_auth_failure(data.username, "invalid_credentials")
        raise HTTPException(status_code=401, detail="Invalid username or password")
    profile, uid = result
    token = create_token(uid)
    return TokenResponse(access_token=token, user=profile)


@router.post("/users", response_model=UserProfile)
def create_new_user(
    data: UserCreate,
    _admin: UserProfile = Depends(require_admin),
):
    """Yalnızca admin yeni kullanıcı oluşturabilir."""
    return create_user(data)


@router.get("/me", response_model=UserProfile)
def me(current_user: UserProfile = Depends(get_current_user)):
    return current_user


@router.get("/users")
def list_users(_admin: UserProfile = Depends(require_admin)):
    """Tüm çalışanları listele — yalnızca admin."""
    from app.core.auth import _load_users
    users = _load_users()
    result = []
    for uid, u in users.items():
        result.append({
            "id": uid,
            "first_name": u.get("first_name", ""),
            "last_name": u.get("last_name", ""),
            "username": u.get("username", ""),
            "area": u.get("area", ""),
            "experience_level": u.get("experience_level", ""),
            "language": u.get("language", "tr"),
            "role": u.get("role", "employee"),
            "notes": u.get("notes", []),
        })
    return result
