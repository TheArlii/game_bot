from app.config import ADMIN_IDS

def is_admin(user_id: int) -> bool:
    try:
        return int(user_id) in ADMIN_IDS
    except:
        return False
