import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from app.config import BOT_TOKEN
from app.router import setup_routers

# Botni ishga tushiruvchi asosiy fayl

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    setup_routers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
