from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.states_fsm import DeleteStates, ChangingData
from core import delete_data, handler_handlers
from core.decorators import with_data
from core.delete_data import handle_show_or_delete_request, delete_data_from_db, delete_element

delete_router = Router()

@delete_router.message(DeleteStates.waiting_for_delete_or_display)
@with_data
async def get_answer_about_delete_or_show(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state,instance, handle_show_or_delete_request
    )


@delete_router.message(DeleteStates.waiting_for_deletion_data_type)
@with_data
async def delete_data(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, delete_data_from_db
    )
    await state.clear()


@delete_router.message(ChangingData.delete)
@with_data
async def delete(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, delete_element
    )
