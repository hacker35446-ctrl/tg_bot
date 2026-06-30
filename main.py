import asyncio
from aiogram import Bot, Dispatcher
from config import ТОКЕН_ТЕЛЕГРАМА
from handlers import start, weather, currency, timer, ai, numbers
from server import start_server_thread

bot = Bot(token=ТОКЕН_ТЕЛЕГРАМА)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(weather.router)
dp.include_router(currency.router)
dp.include_router(timer.router)
dp.include_router(ai.router)
dp.include_router(numbers.router)

async def main():
    start_server_thread()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())