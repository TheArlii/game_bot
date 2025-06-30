# 📁 keyboards/admin_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 🛠 Admin menyusi uchun tugmalar
admin_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📩 Reklama yuborish")],
        [KeyboardButton(text="📊 Statistika")],
        [KeyboardButton(text="➕ Lavozim berish")],
        [KeyboardButton(text="🔍 ID orqali foydalanuvchini izlash")],
        [KeyboardButton(text="📌 Majburiy obuna sozlamalari")],
        [KeyboardButton(text="🚀 Push xabar yuborish")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Admin menyudan birini tanlang..."
)
