
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from click import echo

from bot.states_fsm import ChangingData
from core import handler_handlers, add_data
from core.add_data import add_data_in_instance
from core.decorators import with_data

add_router = Router()

@add_router.message(ChangingData.add)
@with_data
async def add(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, add_data_in_instance
    )

@add_router.message()
async def echo(message:Message):
    await message.answer('/help')