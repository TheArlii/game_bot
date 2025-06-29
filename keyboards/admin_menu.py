# keyboards/admin_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 🛠 Admin menyusi tugmalari
admin_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📩 Reklama yuborish")],            # 1. Reklama
        [KeyboardButton(text="📊 Statistika")],                  # 2. Statistika
        [KeyboardButton(text="➕ Lavozim berish")],              # 3. Lavozim berish
        [KeyboardButton(text="🔍 ID orqali foydalanuvchini izlash")],  # 4. Foydalanuvchini ID bo‘yicha izlash
        [KeyboardButton(text="📌 Majburiy obuna sozlamalari")],  # 5. Majburiy reklama (link)
        [KeyboardButton(text="🚀 Push xabar yuborish")]           # 6. Push xabar
    ],
    resize_keyboard=True
)
