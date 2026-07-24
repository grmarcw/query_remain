import os

from aiogram.fsm import storage
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')

bot = Bot(token=bot_token)
storage = MemoryStorage()
router = Router()
dp = Dispatcher(storage=storage)
