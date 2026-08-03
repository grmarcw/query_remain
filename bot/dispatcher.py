import asyncio
import os

from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from bot.initial.changing_data import router_changing
from bot.initial.delete_data import delete_router
from bot.initial.main_handlers import main_router

from bot.initial.add_data import add_router
from bot.initial.prompts import prompt_router

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(main_router)
dp.include_router(router_changing)
dp.include_router(delete_router)
dp.include_router(add_router)
dp.include_router(prompt_router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Бот запущен")
    asyncio.run(main())
