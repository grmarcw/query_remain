from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.buttons import (
    buttons_yes_or_not
)
from bot.states_fsm import States, FillingStates, CurrentActualBalance
from core import renderers, main, check_data, handler_handlers
from core.decorators import with_data

main_router = Router()


@main_router.message(FillingStates.waiting_for_data_list)
@with_data
async def get_list_ingredients(message: Message, state: FSMContext, instance):
    user_answer = renderers.convert_string_to_list(message.text)
    instance.ingredients = user_answer
    await state.update_data(instance=instance)
    await message.answer(text=renderers.render_list(user_answer, instance.data_filling_stage), reply_markup=buttons_yes_or_not())
    await state.set_state(FillingStates.waiting_for_data_confirmation)


@main_router.message(FillingStates.waiting_for_data_confirmation)
@with_data
async def check_correctness_data(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance,check_data.give_response_text_for_check_correctness_data
    )

@main_router.message(FillingStates.waiting_for_data_for_composition)
@with_data
async def get_position_list(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, main.get_composition
    )


@main_router.message(FillingStates.waiting_quantity)
@with_data
async def get_quantity(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, main.get_quantity_ingredients
    )


@main_router.message(States.waiting_save_confirmation)
@with_data
async def saving_data(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, main.saving
    )

@main_router.message(FillingStates.waiting_for_delivery_data_composition)
@with_data
async def get_position_list(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, main.get_delivery_composition
    )


@main_router.message(FillingStates.waiting_for_filling_data_confirmation)
@with_data
async def get_position_list(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, check_data.get_confirm
    )

@main_router.message(CurrentActualBalance.waiting_for_quantity)
@with_data
async def get_position_list(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, main.get_quantity_balance
    )