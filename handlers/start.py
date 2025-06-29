# 📁 handlers/start.py

import json
import os
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import main_menu

router = Router()
USERS_DB = "users.json"

@router.message(lambda m: m.text == "/start")
async def start_handler(message: Message, bot: Bot, state: FSMContext):
    user_id = str(message.from_user.id)
    full_name = message.from_user.full_name

    # 🧹 Yuborilgan /start xabarini o‘chirish
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

    # ✅ Foydalanuvchini bazaga qo‘shish yoki tekshirish
    if not os.path.exists(USERS_DB):
        with open(USERS_DB, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(USERS_DB, "r", encoding="utf-8") as f:
        users = json.load(f)

    if user_id not in users:
        users[user_id] = {
            "name": full_name,
            "points": 0,
            "wins": 0,
            "loses": 0,
            "invites": 0
        }
        with open(USERS_DB, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    # ✅ Asosiy menyuni yuborish
    msg = await message.answer(
        "🏁 <b>Xush kelibsiz!</b>\n\nAsosiy menyudan birini tanlang:",
        reply_markup=main_menu(int(user_id))
    )

    await state.update_data(last_msg_id=msg.message_id)
