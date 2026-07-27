import asyncio
import os

from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    print('Бот запущен')
    asyncio.run(main())
