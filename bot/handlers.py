import asyncio

from aiogram import types

from bot.dispatcher import dp, router, bot


@router.message()
async def echo(message: types.Message):
    await message.answer('я пока ничего не умею')


dp.include_router(router)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())