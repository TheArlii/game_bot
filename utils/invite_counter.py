import json
import os

USER_DB_PATH = "users.json"

def get_invite_count(user_id: int) -> int:
    """
    Foydalanuvchi (user_id) tomonidan taklif qilingan do‘stlar sonini hisoblaydi.
    """
    if not os.path.exists(USER_DB_PATH):
        return 0

    try:
        with open(USER_DB_PATH, "r", encoding="utf-8") as f:
            users = json.load(f)

        count = 0
        for user in users.values():
            if str(user.get("ref")) == str(user_id):
                count += 1

        return count

    except Exception as e:
        print(f"[XATO] Takliflar sonini olishda muammo: {e}")
        return 0
