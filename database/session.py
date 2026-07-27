import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.engine import create_async_engine

load_dotenv()

url = os.getenv("DB_URL")

engine = create_async_engine(url)

session_maker = async_sessionmaker(engine)
