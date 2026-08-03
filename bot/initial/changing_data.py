from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.states_fsm import  ChangingData
from core import change_data, handler_handlers
from core.decorators import with_data

router_changing = Router()

@router_changing.message(ChangingData.waiting_element_for_change)
@with_data
async def get_answer_about_change(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, change_data.get_element_for_change
    )



@router_changing.message(ChangingData.change)
@with_data
async def change(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, change_data.change_data
    )


@router_changing.message(ChangingData.waiting_ingredient_name)
@with_data
async def choose_composition_for_change(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, change_data.get_composition_for_change
    )


@router_changing.message(ChangingData.recomposition)
@with_data
async def recomposite(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, change_data.recomposites
    )


@router_changing.message(ChangingData.waiting_position_name_for_change)
@with_data
async def get_position_for_change(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, change_data.get_position_name_for_change
    )


@router_changing.message(ChangingData.waiting_new_quantity)
@with_data
async def get_new_quantity(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, change_data.change_quantity
    )
