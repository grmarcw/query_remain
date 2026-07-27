import asyncio

from database.session import engine
from database.models import User, Base


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(create_tables())
