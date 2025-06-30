from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(lambda m: m.text == "🔒 Web App kirish")
async def check_subscription(message: Message, bot: Bot, state: FSMContext):
    await message.answer(
        "⛔ <b>Obuna bo‘lmagan foydalanuvchilar uchun kirish cheklangan.</b>\n"
        "🔧 Ushbu bo‘lim tez orada ishga tushadi."
    )
