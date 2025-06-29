from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import main_menu

router = Router()

# 🔙 Orqaga tugmasi uchun handler
@router.message(lambda m: m.text == "🔙 Orqaga")
async def back_handler(message: Message, bot: Bot, state: FSMContext):
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except: pass

    data = await state.get_data()
    msg_id = data.get("last_msg_id")
    if msg_id:
        try:
            await bot.delete_message(message.chat.id, msg_id)
        except: pass

    msg = await message.answer("🏠 Asosiy menyu:", reply_markup=main_menu)
    await state.update_data(last_msg_id=msg.message_id)
