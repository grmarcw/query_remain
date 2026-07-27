from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

import constants
from bot.handlers.buttons import buttons_show_delete, buttons_yes_or_not
from bot.states_fsm import States, DeleteFromDB
from core import logic
from database import queries

main_router = Router()


@main_router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    user = message.from_user

    if await queries.get_user_data(user.id) is None:
        await message.answer(
            constants.ASK_LIST_INGREDIENTS, reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(States.waiting_ingredient_list)
    elif await queries.get_user_data(user.id) is not None:
        await message.answer(
            "В базе найдены данные\nХотите отобразить данные или удалить?",
            reply_markup=buttons_show_delete(),
        )
        await state.set_state(DeleteFromDB.waiting_for_change_decision_from_db)


@main_router.message(DeleteFromDB.waiting_for_change_decision_from_db)
async def get_answer_about_delete_or_show(message: Message, state: FSMContext):
    us_answer = message.text.lower()

    if us_answer == "удалить" or us_answer == "удалить данные":
        await message.answer(
            "Данные невозможно будет восттановить\nВы уверены, что хотите их удалить безвозвратно?",
            reply_markup=buttons_yes_or_not(),
        )
        await state.set_state(DeleteFromDB.waiting_ans_about_delete_data_from_db)
    elif us_answer == "отобразить" or us_answer == "отобразить данные":
        user = message.from_user
        data = await queries.get_user_data(user.id)
        await message.answer(
            logic.show_recipes(data.recipes), reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state()
    elif message.text.lower() == "да":
        await message.answer(
            "Пожалуйста, напишите, вы хотите отобразить или удалить данные\nДля отмены напишите любое слово"
        )
    else:
        await message.answer("Отменяю операцию", reply_markup=ReplyKeyboardRemove())


@main_router.message(DeleteFromDB.waiting_ans_about_delete_data_from_db)
async def delete_data(message: Message, state: FSMContext):
    user = message.from_user
    await queries.delete_user(user.id)
    await message.answer("Данные удалены", reply_markup=ReplyKeyboardRemove())
    await state.clear()
