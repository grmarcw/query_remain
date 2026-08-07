from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import constants
from bot.buttons import buttons_show_delete
from bot.states_fsm import ChangingData, DeleteStates
from constants.constants import INPUT_START
from core import check_data, handler_handlers, clarification_date
from bot.context import InitialData, DailyData
from core.decorators import with_data

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
    delete_show = '/delete_or_show - для удаления данных или отображения\n'
    input_daily_data = '/input_daily_data - для ввода информации о расхода/дохода продукции\n'
    await message.answer(start+cancel+delete_show+input_daily_data)

@prompt_router.message(Command('delete_or_show'))
async def delete_or_show(message: Message, state: FSMContext):
    instance = InitialData()
    instance.id_user = message.from_user.id
    await state.update_data(instance=instance)
    await message.answer(constants.constants.SHOW_OR_DELETE, reply_markup=buttons_show_delete())
    await state.set_state(DeleteStates.waiting_for_delete_or_display)

@prompt_router.message(Command('input_daily_data'))
async def input_daily_data(message: Message, state: FSMContext):
    instance = DailyData()
    instance.id_user = message.from_user.id
    await state.update_data(instance=instance)
    result = clarification_date.clarification(instance)
    text, button_config, next_state = result
    await message.answer(text, reply_markup=button_config)
    await state.set_state(next_state)

