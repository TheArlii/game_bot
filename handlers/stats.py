from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.back import back_menu
import json
import os

router = Router()

@router.message(lambda m: m.text == "🏆 Reyting")
async def stats(message: Message, bot: Bot, state: FSMContext):
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

    # 📖 Foydalanuvchilarni o‘qib olish
    users = {}
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        except:
            pass

    # 📈 Reytingni ball bo‘yicha saralash
    reyting = sorted(users.items(), key=lambda item: item[1].get("points", 0), reverse=True)
    top10 = reyting[:10]

    reyting_text = "🏆 <b>Top 10 foydalanuvchi:</b>\n\n"
    user_rank = None

    for i, (uid, data) in enumerate(top10, start=1):
        name = data.get("name", "Noma’lum")
        point = data.get("points", 0)
        reyting_text += f"{i}. <b>{name}</b> — {point} ball\n"

    # 👤 Foydalanuvchi o‘rnini topamiz
    if user_id in [uid for uid, _ in top10]:
        user_rank = [uid for uid, _ in top10].index(user_id) + 1
    else:
        for i, (uid, data) in enumerate(reyting, start=1):
            if uid == user_id:
                user_rank = i
                break

    if user_rank:
        reyting_text += f"\n👤 Sizning o‘rningiz: <b>{user_rank}-o‘rin</b>"
    else:
        reyting_text += "\n👤 Siz hali reytingga kirmagansiz."

    # 📩 Natijani yuborish
    msg = await message.answer(reyting_text, reply_markup=back_menu)
    await state.update_data(last_msg_id=msg.message_id)
