# keyboards/main_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.config import ADMIN_IDS  # Adminlarni tekshirish uchun kerak

def main_menu(user_id: int) -> ReplyKeyboardMarkup:
    """
    Asosiy menyuni foydalanuvchi ID asosida dinamik quradi.
    Adminlar uchun qo‘shimcha tugmalar ko‘rsatiladi.
    """

    # 📋 Oddiy foydalanuvchilar uchun umumiy menyu
    buttons = [
        [KeyboardButton(text="👤 Profil")],
        [KeyboardButton(text="🎮 O‘yinlar")],
        [KeyboardButton(text="🎁 Ballarni almashtirish")],
        [KeyboardButton(text="📈 Reyting")],
        [KeyboardButton(text="🤝 Do‘st taklif qilish")],
        [KeyboardButton(text="ℹ️ Bot haqida")]
    ]

    # 🛠 Adminlar uchun alohida tugma
    if user_id in ADMIN_IDS:
        buttons.append([KeyboardButton(text="⚙️ Admin paneli")])

    # 🏅 Lavozimga qarab tugmalar (keyinchalik bu yerga qo‘shiladi)

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Kerakli menyuni tanlang..."
    )
