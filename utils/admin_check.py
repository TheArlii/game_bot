# 📁 utils/admin_check.py

from app.config import ADMIN_IDS

# ✅ Adminligini tekshiruvchi funksiya
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS
