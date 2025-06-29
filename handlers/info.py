from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.back import back_menu  # 🔙 Orqaga qaytish tugmasi

router = Router()

# ℹ️ Bot haqida va qoidalar
@router.message(lambda m: m.text == "ℹ️ Bot haqida / Qoidalar")
async def info_handler(message: Message, bot: Bot, state: FSMContext):
    user_id = str(message.from_user.id)

    # 🧹 Kiruvchi va eski xabarlarni o‘chirish
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except: pass

    data = await state.get_data()
    msg_id = data.get("last_msg_id")
    if msg_id:
        try:
            await bot.delete_message(message.chat.id, msg_id)
        except: pass

    # 📄 Matnni tayyorlash
    text = (
        "<b>ℹ️ Bot haqida / Qoidalar</b>\n\n"
        "🤖 Bu bot orqali siz o‘yin o‘ynab ball to‘plashingiz, do‘stlaringizni taklif qilib ball ishlashingiz va ularni Telegram Premium yoki boshqa sovg‘alarga almashtirishingiz mumkin.\n\n"

        "<b>🎮 O‘yinlar</b>\n"
        "• Ballik o‘yinlar: oddiy mini-o‘yinlar, g‘alaba uchun ball beriladi.\n"
        "• Web app o‘yinlar: premium o‘yinlar, ball tizimi mavjud emas.\n\n"

        "<b>🎁 Ballarni nimalarga almashtirish mumkin?</b>\n"
        "• 300 ball — 1 oylik Telegram Premium\n"
        "• 500 ball — 2 oylik Telegram Premium\n"
        "• 1000 ball — Sirli sovg‘a 🎉\n\n"

        "<b>👥 Referal (do‘st taklif qilish)</b>\n"
        "• Har bir do‘st uchun 1 ball qo‘shiladi.\n"
        "• Taklif havolangiz orqali kirgan foydalanuvchi faqat 1 marta hisoblanadi.\n\n"

        "<b>🏅 Lavozimlar va Imkoniyatlar</b>\n"
        "• Lavozim — bu sizning botdagi maqomingiz.\n"
        "• Admin berishi yoki ball evaziga olinishi mumkin.\n"
        "• Har bir lavozim yangi imkoniyatlar ochadi (bonuslar, tugmalar, kirishlar va h.k).\n\n"

        "<b>⚠️ Qoidalar</b>\n"
        "1. Botdan adolatli foydalaning.\n"
        "2. Ballarni firibgarlik bilan yig‘mang — bloklanasiz.\n"
        "3. Reklama, spam, xakerlik taqiqlanadi.\n"
        "4. Yordam kerak bo‘lsa, admin bilan bog‘laning.\n\n"

        "<i>🎯 Maqsad — o‘yin orqali vaqtni maroqli o‘tkazish va mukofotlar yutib olish!</i>"
    )

    # 📩 Xabar yuborish va yangi xabar ID sini saqlash
    msg = await message.answer(text, reply_markup=back_menu)
    await state.update_data(last_msg_id=msg.message_id)
