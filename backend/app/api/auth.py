import os
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import LoginRequest, TokenResponse, UserCreate, UserProfile
from app.core.auth import authenticate_user, create_token, create_user, require_admin, get_current_user, _load_users, _save_users
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


@router.delete("/users/{user_id}")
def delete_user(
    user_id: str,
    current_admin: UserProfile = Depends(require_admin),
):
    """Kullanıcıyı ve ilerleme verisini sil — yalnızca admin."""
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    users = _load_users()
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    if users[user_id].get("role") == "admin":
        raise HTTPException(status_code=400, detail="Cannot delete another admin account")
    del users[user_id]
    _save_users(users)
    # İlerleme dosyasını da temizle
    from app.content.progress_store import DATA_DIR
    progress_file = os.path.join(DATA_DIR, f"progress_{user_id}.json")
    if os.path.exists(progress_file):
        os.remove(progress_file)
    return {"message": "User deleted"}
