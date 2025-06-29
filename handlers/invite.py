# handlers/invite.py
import json
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.back import back_menu

router = Router()

REFERAL_DB = "data/referallar.json"
USERS_DB = "users.json"

# 🔗 Taklif havolasini ko‘rsatish
@router.message(lambda m: m.text == "👥 Do‘st taklif qilish")
async def referal_handler(message: Message, bot: Bot, state: FSMContext):
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

    # 📥 Taklif havolasini yaratamiz
    username = (await bot.get_me()).username
    link = f"https://t.me/{username}?start={user_id}"

    # 📊 Statistika (nechta do‘st taklif qilgan)
    try:
        with open(REFERAL_DB, "r", encoding="utf-8") as f:
            data = json.load(f)
        count = data.get(user_id, 0)
    except:
        count = 0

    # 📩 Javob matni
    text = (
        f"<b>👥 Do‘st taklif qilish</b>\n\n"
        f"Quyidagi maxsus havolani do‘stlaringizga yuboring:\n\n"
        f"<code>{link}</code>\n\n"
        f"Taklif qilingan har bir do‘st uchun sizga <b>1 ball</b> beriladi.\n"
        f"Hozirga qadar: <b>{count} ta</b> do‘st taklif qilgansiz."
    )

    msg = await message.answer(text, reply_markup=back_menu)
    await state.update_data(last_msg_id=msg.message_id)
