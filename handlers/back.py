from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import main_menu

router = Router()

# 🔙 Orqaga tugmasi uchun handler
@router.message(lambda m: m.text == "🔙 Orqaga")
async def back_handler(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id

    # 🔄 Kiruvchi va eski xabarlarni o‘chirish
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass

    data = await state.get_data()
    msg_id = data.get("last_msg_id")
    if msg_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
        except:
            pass

    # 🏠 Asosiy menyuni qayta yuborish
    msg = await message.answer(
        "🏠 Asosiy menyu:",
        reply_markup=main_menu(user_id)
    )

    await state.update_data(last_msg_id=msg.message_id)
