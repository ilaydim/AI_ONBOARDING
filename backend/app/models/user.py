from pydantic import BaseModel
from typing import Optional
from enum import Enum


class ExperienceLevel(str, Enum):
    junior = "junior"
    mid = "mid"
    senior = "senior"


class Language(str, Enum):
    tr = "tr"
    en = "en"


class UserRole(str, Enum):
    employee = "employee"
    admin = "admin"


class ProfileNote(BaseModel):
    key: str          # ör. "docker"
    value: str        # ör. "Docker bilmiyor"
    verified: bool = False


class UserProfile(BaseModel):
    id: str
    first_name: str
    last_name: str
    area: str                         # ör. "backend"
    experience_level: ExperienceLevel
    language: Language = Language.tr
    role: UserRole = UserRole.employee
    notes: list[ProfileNote] = []


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    area: str
    experience_level: ExperienceLevel
    language: Language = Language.tr
    role: UserRole = UserRole.employee
    notes: list[ProfileNote] = []


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile
