from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

import constants
from bot.states_fsm import States
from database import queries

main_router = Router()

@main_router.message(Command('start'))
async def start(message:Message, state: FSMContext):
    user = message.from_user

    if await queries.get_user_data(user.id) is None:
        await message.answer(constants.ASK_LIST_INGREDIENTS)
        await state.set_state(States.waiting_ingredient_list)
    elif await queries.get_user_data(user.id) is not None:
        await message.answer('В базе найдены данные\nХотите отобразить данные или удалить?')
        await state.set_state(States.waiting_for_change_decision)
