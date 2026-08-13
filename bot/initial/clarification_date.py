from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.states_fsm import CheckDate
from core import clarification_date, handler_handlers
from core.decorators import with_data

clarification_router = Router()


@clarification_router.message(CheckDate.waiting_for_confirm_date)
@with_data
async def check_correctness_data(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, clarification_date.handle_date_confirmation
    )


@clarification_router.message(CheckDate.waiting_for_correct_date)
@with_data
async def check_correctness_data(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, clarification_date.ask_correct_date
    )
