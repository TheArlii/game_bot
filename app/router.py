from aiogram import Dispatcher
from handlers import start, profile, back, games, exchange, stats, admin, subscription

# Barcha handlerlar shu yerga ulangan
def setup_routers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(back.router)
    dp.include_router(games.router)
    dp.include_router(exchange.router)
    dp.include_router(stats.router)
    dp.include_router(admin.router)
    dp.include_router(subscription.router)
