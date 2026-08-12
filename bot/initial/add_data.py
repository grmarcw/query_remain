from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from click import echo

from bot.states_fsm import ChangingData
from core import handler_handlers, add_data
from core.add_data import add
from core.decorators import with_data

add_router = Router()


@add_router.message(ChangingData.add)
@with_data
async def handler_add(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(message, state, instance, add)


@add_router.message(StateFilter(None))
async def echo(message: Message):
    await message.answer("/help")
