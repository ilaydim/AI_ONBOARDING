from fastapi import APIRouter, HTTPException
from app.models.user import LoginRequest, TokenResponse, UserCreate, UserProfile
from app.core.auth import authenticate_user, create_token, create_user, require_admin, get_current_user
from fastapi import Depends

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    result = authenticate_user(data.username, data.password)
    if not result:
        raise HTTPException(status_code=401, detail="Geçersiz kullanıcı adı veya şifre")
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
