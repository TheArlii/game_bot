import json
import os

LAVOZIM_DB = "data/lavozimlar.json"

def get_user_level(user_id: int) -> str:
    """
    Foydalanuvchining lavozimini qaytaradi.
    Agar lavozim mavjud bo‘lmasa, 'Oddiy foydalanuvchi' deb qaytaradi.
    """
    if not os.path.exists(LAVOZIM_DB):
        return "Oddiy foydalanuvchi"

    try:
        with open(LAVOZIM_DB, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(str(user_id), "Oddiy foydalanuvchi")
    except Exception as e:
        print(f"[XATO] Lavozim o‘qishda muammo: {e}")
        return "Oddiy foydalanuvchi"
