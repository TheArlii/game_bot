import json
import os
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.profile import profile_menu

router = Router()

DB_PATH = "users.json"

# ✅ Lavozimni olish
def lavozimni_olish(user_id: str) -> str:
    try:
        with open("data/lavozimlar.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(user_id, "– lavozim belgilanmagan –")
    except:
        return "– lavozim belgilanmagan –"

# ✅ Reytingni olish
def reytingni_olish(user_id: str) -> str:
    try:
        with open("data/reyting.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            user_data = data.get(user_id)
            if not user_data:
                return "– hali reyting yo‘q –"

            win = user_data.get("win", 0)
            lose = user_data.get("lose", 0)
            total = win + lose

            if total == 0:
                return "– hali reyting yo‘q –"

            rating = round((win / total) * 10, 1)
            return f"{rating}/10"
    except:
        return "– hali reyting yo‘q –"

# ✅ Referallar sonini olish
def referallar_soni(user_id: str) -> int:
    try:
        with open("data/referallar.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(user_id, 0)
    except:
        return 0

# 🧾 Profil ko‘rish handler
@router.message(lambda m: m.text == "👤 Profil")
async def profile_handler(message: Message, bot: Bot, state: FSMContext):
    user_id = str(message.from_user.id)

    # 🧹 Kiruvchi xabarni o‘chirish
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    # 🧹 Oldingi bot xabarini o‘chirish
    data = await state.get_data()
    msg_id = data.get("last_msg_id")
    if msg_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
        except:
            pass

    # ✅ Foydalanuvchilar bazasi
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(DB_PATH, "r", encoding="utf-8") as f:
        users = json.load(f)

    if user_id not in users:
        users[user_id] = {
            "name": message.from_user.full_name,
            "games_played": 0,
            "points": 0
        }
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    user = users[user_id]
    lavozim = lavozimni_olish(user_id)
    reyting = reytingni_olish(user_id)
    referallar = referallar_soni(user_id)

    # 📬 Profil ma’lumotini yuborish
    text = (
        f"<b>👤 Profilingiz</b>\n\n"
        f"💻 Ism: <i>{user['name']}</i>\n"
        f"🎯 O‘yinlar: <b>{user['games_played']}</b> ta\n"
        f"💰 Ball: <b>{user['points']}</b> ball\n"
        f"🏅 Lavozim: <b>{lavozim}</b>\n"
        f"🏆 Reyting: <b>{reyting}</b>\n"
        f"👥 Taklif qilganlar: <b>{referallar}</b> ta"
    )

    msg = await message.answer(text, reply_markup=profile_menu)
    await state.update_data(last_msg_id=msg.message_id)
