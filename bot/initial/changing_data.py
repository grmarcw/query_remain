from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.states_fsm import ChangingData
from core import change_data, handler_handlers
from core.check_data import choose_action
from core.decorators import with_data

router_changing = Router()


@router_changing.message(ChangingData.waiting_result_choosing_action)
@with_data
async def get_result_choosing_action(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(message, state, instance, choose_action)


@router_changing.message(ChangingData.waiting_element_for_change)
@with_data
async def handler_get_element_for_change(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, change_data.get_element_for_change
    )


@router_changing.message(ChangingData.change)
@with_data
async def handler_change(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, change_data.change
    )


@router_changing.message(ChangingData.waiting_ingredient_name)
@with_data
async def handler_get_composition_for_change(
    message: Message, state: FSMContext, instance
):
    await handler_handlers.proccess_user_input(
        message, state, instance, change_data.get_composition_for_change
    )
