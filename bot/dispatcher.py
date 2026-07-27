import asyncio
import os

from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from bot.handlers.changing_data import router_changing
from bot.handlers.main_handlers import main_router

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(main_router)
dp.include_router(router_changing)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Бот запущен")
    asyncio.run(main())
