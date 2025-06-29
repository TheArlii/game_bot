# handlers/rating.py
import json
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.back import back_menu  # Orqaga tugmasi

router = Router()

# 📈 Reyting menyusi — TOP 10 + foydalanuvchining o‘rni
@router.message(lambda m: m.text == "📈 Reyting")
async def show_rating(message: Message, bot: Bot, state: FSMContext):
    user_id = str(message.from_user.id)

    # 🧹 Kiruvchi va eski bot xabarlarini o‘chirish
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except: pass

    data = await state.get_data()
    msg_id = data.get("last_msg_id")
    if msg_id:
        try:
            await bot.delete_message(message.chat.id, msg_id)
        except: pass

    # 🔍 Reyting ma'lumotlarini yuklaymiz
    reyting_file = "data/reyting.json"
    reyting = {}
    try:
        with open(reyting_file, "r", encoding="utf-8") as f:
            reyting = json.load(f)
    except:
        pass

    # 🧮 Har bir foydalanuvchining bahosini hisoblaymiz (10 ballik)
    baholar = []
    for uid, stats in reyting.items():
        win = stats.get("win", 0)
        lose = stats.get("lose", 0)
        total = win + lose
        if total == 0:
            continue
        rating = round((win / total) * 10, 2)
        baholar.append((uid, rating))

    # 🔢 Reyting bo‘yicha saralash
    baholar.sort(key=lambda x: x[1], reverse=True)  # Yuqoridan pastga

    # 🥇 TOP 10 ni tayyorlaymiz
    top_text = "<b>📈 TOP 10 Reyting</b>\n\n"
    user_rank = None
    for i, (uid, score) in enumerate(baholar[:10], start=1):
        line = f"{i}. <code>{uid}</code> — <b>{score}/10</b>\n"
        top_text += line

    # 👤 Foydalanuvchining o‘rnini topamiz
    for i, (uid, score) in enumerate(baholar, start=1):
        if uid == user_id:
            user_rank = i
            break

    if user_rank:
        top_text += f"\n👤 Siz reytingda <b>{user_rank}-o‘rindasiz</b>."
    else:
        top_text += "\n👤 Siz hali reytingga kirmagansiz."

    # 📩 Javob yuborish
    msg = await message.answer(top_text, reply_markup=back_menu)
    await state.update_data(last_msg_id=msg.message_id)
