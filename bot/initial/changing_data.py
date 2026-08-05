from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.states_fsm import  ChangingData
from core import change_data, handler_handlers
from core.check_data import choose_action
from core.decorators import with_data

router_changing = Router()

@router_changing.message(ChangingData.waiting_element_for_change)
@with_data
async def get_answer_about_change(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, change_data.get_element_for_change
    )

@router_changing.message(ChangingData.waiting_result_choosing_action)
@with_data
async def get_result_choosing_action(message: Message, state: FSMContext, instance):
    user_answer = message.text.lower()

    result = choose_action(user_answer, instance)
    text, buttons_config, next_state = result
    await state.update_data(instance=instance)

    await message.answer(text, reply_markup=buttons_config)
    if next_state:
        await state.set_state(next_state)


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
