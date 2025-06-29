# keyboards/games_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

games_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎯 Ballik o‘yinlar")],
        [KeyboardButton(text="🕹 Web app o‘yinlar")],
        [KeyboardButton(text="🔙 Orqaga")]
    ],
    resize_keyboard=True
)
