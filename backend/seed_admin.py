"""
İlk admin kullanıcısını oluşturur.
Kullanım: python seed_admin.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.auth import create_user
from app.models.user import UserCreate, UserRole, ExperienceLevel, Language

admin = UserCreate(
    first_name="Admin",
    last_name="TechNova",
    username="admin",
    password="admin123",     # Demo için basit şifre — üretimde değiştir!
    area="backend",
    experience_level=ExperienceLevel.senior,
    language=Language.tr,
    role=UserRole.admin,
)

user = create_user(admin)
print(f"✅ Admin oluşturuldu: username=admin, password=admin123, id={user.id}")
