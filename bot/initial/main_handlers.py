from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.states_fsm import States, FillingStates, CurrentActualBalance, Main
from core import main, check_data, handler_handlers
from core.decorators import with_data

main_router = Router()


@main_router.message(FillingStates.waiting_for_data_list)
@with_data
async def handler_get_data_list(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, main.get_data_list
    )


@main_router.message(FillingStates.waiting_for_data_confirmation)
@with_data
async def handler_check_correctness_data(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, check_data.check_correctness_data
    )


@main_router.message(FillingStates.waiting_for_products_list)
@with_data
async def handler_get_products(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, main.get_products
    )


@main_router.message(FillingStates.waiting_for_data_for_composition)
@with_data
async def handler_get_composition(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, main.get_composition
    )


@main_router.message(FillingStates.waiting_quantity)
@with_data
async def handler_get_quantity(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, main.get_quantity
    )


@main_router.message(States.waiting_save_confirmation)
@with_data
async def saving_data(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(message, state, instance, main.saving)


@main_router.message(FillingStates.waiting_for_delivery_data_composition)
@with_data
async def get_position_list(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, main.get_delivery_composition
    )


@main_router.message(CurrentActualBalance.waiting_for_quantity)
@with_data
async def get_position_list(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, main.get_quantity_balance
    )


@main_router.message(Main.waiting_for_quantity_sold)
@with_data
async def get_sold_product_quantity(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, main.get_quantity_balance
    )


@main_router.message(Main.waiting_for_deliveries_names)
@with_data
async def get_deliveries_names(message: Message, state: FSMContext, instance):
    await handler_handlers.proccess_user_input(
        message, state, instance, main.get_products
    )
