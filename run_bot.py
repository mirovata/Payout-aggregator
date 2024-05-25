import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import router

dp = Dispatcher()


async def main():
    load_dotenv()
    bot = Bot(os.getenv('TELEGRAM_TOKEN'))
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
