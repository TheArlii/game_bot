import json, os
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.profile import profile_menu

# Router obyektini yaratamiz (profil uchun)
router = Router()

# 📁 Foydalanuvchi asosiy bazasi
DB_PATH = "users.json"

# ✅ Lavozimni olish funksiyasi (data/lavozimlar.json dan)
def lavozimni_olish(user_id: str) -> str:
    try:
        with open("data/lavozimlar.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # Agar lavozim topilmasa default yozuv chiqariladi
            return data.get(user_id, "– lavozim belgilanmagan –")
    except:
        return "– lavozim belgilanmagan –"

# ✅ Reytingni olish funksiyasi (data/reyting.json dan)
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

            # G‘alabalar nisbati asosida 10 ballik tizimda baholanadi
            rating = round((win / total) * 10, 1)
            return f"{rating}/10"
    except:
        return "– hali reyting yo‘q –"

# ✅ Referal sonini olish funksiyasi (data/referallar.json dan)
def referallar_soni(user_id: str) -> int:
    try:
        with open("data/referallar.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(user_id, 0)
    except:
        return 0

# 🧾 Profil ko‘rish uchun asosiy handler
@router.message(lambda m: m.text == "👤 Profil")
async def profile_handler(message: Message, bot: Bot, state: FSMContext):
    user_id = str(message.from_user.id)

    # 🔄 So‘nggi xabarlarni o‘chirish (tozalik uchun)
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    data = await state.get_data()
    msg_id = data.get("last_msg_id")
    if msg_id:
        try:
            await bot.delete_message(message.chat.id, msg_id)
        except:
            pass

    # 📂 Agar userlar bazasi mavjud bo‘lmasa — yaratish
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f)

    # 📖 Foydalanuvchilarni o‘qib olish
    with open(DB_PATH, "r", encoding="utf-8") as f:
        users = json.load(f)

    # 🌱 Agar foydalanuvchi bazada bo‘lmasa — yangi yozuv qo‘shamiz
    if user_id not in users:
        users[user_id] = {
            "name": message.from_user.full_name,
            "games_played": 0,
            "points": 0
        }
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(users, f)

    user = users[user_id]

    # 🧙‍♂️ Qo‘shimcha ma'lumotlarni olish
    lavozim = lavozimni_olish(user_id)
    reyting = reytingni_olish(user_id)
    referallar = referallar_soni(user_id)

    # 🎨 Foydalanuvchi profili dizayni
    text = (
        f"<b>👤 Profilingiz</b>\n\n"
        f"💻 Ism: <i>{user['name']}</i>\n"
        f"🎯 O‘yinlar: <b>{user['games_played']}</b> ta\n"
        f"💰 Ball: <b>{user['points']}</b> ball\n"
        f"🏅 Lavozim: <b>{lavozim}</b>\n"
        f"🏆 Reyting: <b>{reyting}</b>\n"
        f"👥 Taklif qilganlar: <b>{referallar}</b> ta"
    )

    # 📬 Javob yuborish va holatni yangilash
    msg = await message.answer(text, reply_markup=profile_menu)
    await state.update_data(last_msg_id=msg.message_id)
