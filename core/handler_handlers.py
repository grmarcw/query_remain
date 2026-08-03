import inspect

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.states_fsm import States
from core.decorators import with_data

async def proccess_user_input(
        message:Message,
        state: FSMContext,
        instance,
        function
):

    user_answer = message.text.lower()
    if inspect.iscoroutinefunction(function):
        text, buttons_config, next_state = await function(user_answer, instance)
    else:
        text, buttons_config, next_state = function(user_answer, instance)
    await state.update_data(instance=instance)

    await message.answer(text, reply_markup=buttons_config)
    if next_state:
        await state.set_state(next_state)
    if next_state == States.clear:
        await state.clear()