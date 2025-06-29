import json
import os

USER_DATA_PATH = "users.json"

def calculate_win_rating(user_id: int) -> int:
    """
    Foydalanuvchining oddiy o‘yinlardagi win ratingini hisoblaydi.
    Reyting 0 dan 10 gacha bo‘ladi.
    Web app o‘yinlar hisobga olinmaydi.
    """
    if not os.path.exists(USER_DATA_PATH):
        return 0  # Foydalanuvchi yo‘q bo‘lsa, 0 qaytariladi

    try:
        with open(USER_DATA_PATH, "r", encoding="utf-8") as f:
            users = json.load(f)

        user = users.get(str(user_id))
        if not user:
            return 0

        wins = int(user.get("wins", 0))
        losses = int(user.get("losses", 0))
        total = wins + losses

        if total == 0:
            return 0  # Reyting bo‘lmagan foydalanuvchi uchun

        # Win rate: 10 ballik tizim asosida
        ratio = wins / total
        rating = round(ratio * 10)
        return min(10, max(0, rating))

    except Exception as e:
        print(f"[XATO] Win rating hisoblashda muammo: {e}")
        return 0
