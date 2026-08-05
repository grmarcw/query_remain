from functools import wraps

from aiogram.fsm.context import FSMContext
from aiogram.types import Message


def with_data(handler):

    @wraps(handler)
    async def wrapper(message: Message, state: FSMContext):
        data = await state.get_data()
        instance = data.get('instance')

        result = await handler(message, state, instance)

        return result

    return wrapper
