from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.util import await_only

from bot.context import RecipesData
from bot.states_fsm import ChangingData
from core import change_data, check_data
from core.decorators import with_data
from core.check_data import init_user_data, choose_action

prompt_router = Router()


@prompt_router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    user = message.from_user

    user_id = user.id
    instance = RecipesData()
    check_data.init_user_data(instance)
    instance.id_user = user_id
    await state.update_data(instance=instance)

    text, buttons_config, next_state = await check_data.check_data_in_db(instance)


    await message.answer(text, reply_markup=buttons_config)
    await state.set_state(next_state)


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