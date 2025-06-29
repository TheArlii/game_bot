from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.games_menu import games_menu  # ✅ O‘yinlar uchun tugmalar
from keyboards.back import back_menu         # 🔙 Orqaga qaytish tugmasi

router = Router()

# 🎮 O‘yinlar menyusini ko‘rsatish
@router.message(lambda m: m.text == "🎮 O‘yinlar")
async def games_menu_handler(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id

    # 🧹 Kiruvchi xabarni o‘chirish
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    # 🧹 Oldingi bot yuborgan xabarni o‘chirish
    data = await state.get_data()
    msg_id = data.get("last_msg_id")
    if msg_id:
        try:
            await bot.delete_message(message.chat.id, msg_id)
        except:
            pass

    # 📩 Yangi xabar: O‘yinlar menyusi
    msg = await message.answer(
        "🎮 <b>O‘yinlar menyusi</b>\n\n👇 Quyidagi turlardan birini tanlang:",
        reply_markup=games_menu  # 🕹 Tugmalar: Ballik o‘yinlar / Web app
    )

    await state.update_data(last_msg_id=msg.message_id)
