from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import constants
from bot.buttons import buttons_show_delete
from bot.states_fsm import ChangingData, DeleteStates
from constants.constants import INPUT_START
from core import check_data
from core.decorators import with_data
from core.check_data import choose_action
from bot.context import InitialData

prompt_router = Router()


@prompt_router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    user = message.from_user

    user_id = user.id
    instance = InitialData
    check_data.init_user_data(instance)
    instance.id_user = user_id
    await state.update_data(instance=instance)

    text, buttons_config, next_state = await check_data.check_data_in_db(instance)


    await message.answer(text, reply_markup=buttons_config)
    await state.set_state(next_state)


@prompt_router.message(Command('cancel'))
async def cancel(message: Message, state: FSMContext):
    await message.answer(INPUT_START)
    await state.clear()

@prompt_router.message(Command('help'))
async def help(message: Message, state: FSMContext):
    start = '/start - для начала заполнения данных\n'
    cancel = '/cancel - для отмены заполнения данных\n'
    delete_show = '/delete_or_show - для удаления данных или отображения'
    await message.answer(start+cancel+delete_show)

@prompt_router.message(Command('delete_or_show'))
async def delete_or_show(message: Message, state: FSMContext):
    instance = InitialData()
    instance.id_user = message.from_user.id
    await state.update_data(instance=instance)
    await message.answer(constants.constants.SHOW_OR_DELETE, reply_markup=buttons_show_delete())
    await state.set_state(DeleteStates.waiting_for_delete_or_display)


@prompt_router.message(ChangingData.waiting_result_choosing_action)
@with_data
async def get_result_choosing_action(message: Message, state: FSMContext, instance):
    user_answer = message.text.lower()

    result = choose_action(user_answer, instance)
    text, buttons_config, next_state = result
    await state.update_data(instance=instance)

    await message.answer(text, reply_markup=buttons_config)
    if next_state:
        await state.set_state(next_state)