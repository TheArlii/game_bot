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

    # 🧹 So‘nggi xabarlarni tozalash
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

    # 📖 Foydalanuvchilar ro‘yxatini o‘qiymiz
    users = {}
    if os.path.exists("users.json"):
        with open("users.json", "r", encoding="utf-8") as f:
            users = json.load(f)

    # 📈 Reytingni ball bo‘yicha saralab chiqaramiz
    reyting = sorted(users.items(), key=lambda item: item[1].get("points", 0), reverse=True)
    top10 = reyting[:10]

    reyting_text = "🏆 <b>Top 10 foydalanuvchi:</b>\n\n"
    user_rank = None
    for i, (uid, data) in enumerate(top10, start=1):
        name = data.get("name", "Noma’lum")
        point = data.get("points", 0)
        reyting_text += f"{i}. <b>{name}</b> — {point} ball\n"

    # 👤 Agar foydalanuvchi reytingda bo‘lmasa, o‘z o‘rnini ko‘rsatamiz
    if user_id in [uid for uid, _ in top10]:
        user_rank = [uid for uid, _ in top10].index(user_id) + 1
    else:
        for i, (uid, data) in enumerate(reyting, start=1):
            if uid == user_id:
                user_rank = i
                break

    if user_rank:
        reyting_text += f"\nSizning o‘rningiz: <b>{user_rank}-o‘rin</b>"
    else:
        reyting_text += "\nSiz hali reytingga kirmagansiz."

    # 📤 Xabarni yuborish
    msg = await message.answer(reyting_text, reply_markup=back_menu)
    await state.update_data(last_msg_id=msg.message_id)
