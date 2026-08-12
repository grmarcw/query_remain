from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

import constants
from bot.buttons import buttons_show_delete
from bot.states_fsm import DeleteStates
from constants import general
from constants.general import INPUT_START
from core import clarification_date, check_data, format_data_from_db, renderers, calc_balance
from bot.context import DataForStates
from database import queries
from database.models import SecondaryData

prompt_router = Router()


@prompt_router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    user = message.from_user

    id_user = user.id
    instance = DataForStates()
    instance.user_id = id_user

    await state.update_data(instance=instance)

    text, buttons, next_state = await check_data.check_data_in_db(instance)
    await message.answer(text, reply_markup=buttons)
    await state.set_state(next_state)


@prompt_router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await message.answer(INPUT_START)
    await state.clear()


@prompt_router.message(Command("help"))
async def help(message: Message):
    start = "/start - для начала заполнения первичных данных\n"
    cancel = "/cancel - для отмены заполнения данных\n"
    delete_show = "/delete_or_show - для удаления данных или отображения\n"
    input_daily_data = "/input_daily_data - для заполнения основных данных\n"
    show_balance = '/show_balance - показать фактический остаток\n'
    await message.answer(start + cancel + delete_show + input_daily_data + show_balance)


@prompt_router.message(Command("delete_or_show"))
async def delete_or_show(message: Message, state: FSMContext):
    instance = DataForStates()
    instance.user_id = message.from_user.id
    await state.update_data(instance=instance)
    await message.answer(
        constants.general.SHOW_OR_DELETE, reply_markup=buttons_show_delete()
    )
    await state.set_state(DeleteStates.waiting_for_delete_or_display)


@prompt_router.message(Command("input_daily_data"))
async def input_daily_data(message: Message, state: FSMContext):
    instance = DataForStates()
    instance.user_id = message.from_user.id

    instance.survey_stage = 8
    await state.update_data(instance=instance)

    text = await check_data.check_data_in_db(instance)
    if text[0] != f"Все первичные данные заполнены":
        await message.answer("/start", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        result = clarification_date.clarification(instance)
        text, button_config, next_state = result
        await message.answer(text, reply_markup=button_config)
        await state.set_state(next_state)


@prompt_router.message(Command("show_balance"))
async def show_balance(message: Message, state: FSMContext):
    instance = DataForStates()
    instance.user_id = message.from_user.id
    data_from_initial = await queries.get_user_data(instance.user_id)
    data_from_secondary = await queries.get_user_data(instance.user_id, SecondaryData)

    if data_from_initial is None:
        await message.answer(f'Для вывода фактического остатка необходимо заполнить данные\n/start')
    elif data_from_secondary is None:
        await message.answer(f'Для вывода фактического остатка необходимо заполнить данные\n/start')
    elif data_from_secondary.data is None:
        await message.answer(f"""Фактический остаток:
{general.SEPARATOR}
{renderers.render_list_or_dict(
            data_from_secondary.initial_balance, 7, option= 2
        )}""")
    else:
        format_data_from_db.format(instance, data_from_initial)

        instance.data_dict = data_from_secondary.initial_balance
        instance.recipes = data_from_initial.recipes
        daily_data_list = data_from_secondary.data

        result = calc_balance.get_actual_balance(daily_data_list, instance)

        await (message.answer(f"""Фактический остаток:
{general.SEPARATOR}
{renderers.render_list_or_dict(result, 7, option=2)}""",
                              reply_markup=ReplyKeyboardRemove()))

    await state.clear()






