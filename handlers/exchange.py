from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.back import back_menu
import json
import os

router = Router()

# 🎁 Ballarni sovg‘alarga almashtirish menyusi
@router.message(lambda m: m.text == "🎁 Ball almashtirish")
async def exchange(message: Message, bot: Bot, state: FSMContext):
    user_id = str(message.from_user.id)

    # 🧹 Foydalanuvchi yuborgan xabarni o‘chirish
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

    # 📖 Foydalanuvchi ballini olish
    user_points = 0
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
                user = users.get(user_id, {})
                user_points = user.get("points", 0)
        except:
            pass

    # 📋 Xabar matni
    text = (
        f"<b>🎁 Ball almashtirish</b>\n\n"
        f"Sizda: <b>{user_points} ball</b> mavjud.\n\n"
        f"Quyidagilarga almashtirishingiz mumkin:\n"
        f"▪️ 300 ball — 1 oylik Telegram Premium\n"
        f"▪️ 500 ball — 2 oylik Telegram Premium\n"
        f"▪️ 1000 ball — Sirli sovg‘a 🎉\n\n"
        f"<i>Almashtirish uchun admin bilan bog‘laning yoki avtomatik tizim tez orada qo‘shiladi.</i>"
    )

    # 📩 Javob yuborish
    msg = await message.answer(text, reply_markup=back_menu)
    await state.update_data(last_msg_id=msg.message_id)
