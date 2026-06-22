import bcrypt
import json
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.settings import get_settings
from app.models.user import UserProfile, UserCreate, UserRole

USERS_FILE = os.path.join(os.path.dirname(__file__), "../../data/users.json")
security = HTTPBearer()


def _load_users() -> dict:
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE) as f:
        return json.load(f)


def _save_users(users: dict):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_token(user_id: str) -> str:
    settings = get_settings()
    expire = datetime.utcnow() + timedelta(minutes=settings.token_expire_minutes)
    return jwt.encode({"sub": user_id, "exp": expire}, settings.secret_key, algorithm="HS256")


def get_user_by_username(username: str) -> tuple[dict, str] | None:
    """Returns (user_dict, user_id) or None"""
    users = _load_users()
    for uid, u in users.items():
        if u.get("username") == username:
            return u, uid
    return None


def authenticate_user(username: str, password: str) -> tuple[UserProfile, str] | None:
    result = get_user_by_username(username)
    if not result:
        return None
    user_dict, uid = result
    if not verify_password(password, user_dict["password_hash"]):
        return None
    profile = UserProfile(**{k: v for k, v in user_dict.items()
                             if k not in ("username", "password_hash")}, id=uid)
    return profile, uid


def create_user(data: UserCreate) -> UserProfile:
    users = _load_users()
    # username unique kontrolü
    for u in users.values():
        if u.get("username") == data.username:
            raise HTTPException(status_code=400, detail="Username already exists")

    import uuid
    uid = str(uuid.uuid4())
    user_record = {
        "username": data.username,
        "password_hash": hash_password(data.password),
        "first_name": data.first_name,
        "last_name": data.last_name,
        "area": data.area,
        "experience_level": data.experience_level,
        "language": data.language,
        "role": data.role,
        "notes": [n.model_dump() for n in data.notes],
    }
    users[uid] = user_record
    _save_users(users)
    return UserProfile(**{k: v for k, v in user_record.items()
                          if k not in ("username", "password_hash")}, id=uid)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserProfile:
    settings = get_settings()
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=["HS256"])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    users = _load_users()
    if user_id not in users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    u = users[user_id]
    return UserProfile(**{k: v for k, v in u.items()
                          if k not in ("username", "password_hash")}, id=user_id)


def require_admin(current_user: UserProfile = Depends(get_current_user)) -> UserProfile:
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin required")
    return current_user
