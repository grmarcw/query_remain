from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

import constants
from bot.handlers.buttons import (
    buttons_choose_action,
    buttons_yes_or_not,
    button_generator,
)
from bot.states_fsm import States, ChangingData
from core import logic

router_changing = Router()


@router_changing.message(ChangingData.waiting_result_choosing_action)
async def get_result_choosing_action(message: Message, state: FSMContext):
    user_answer = message.text.lower()
    data = await state.get_data()

    current_stage = data.get("survey_stage")
    ingredient_list = data.get("ingredient_list")
    if user_answer == "поменять позицию":
        if current_stage == 1:
            await message.answer(
                "Какую позицию вы хотите изменить?", reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(ChangingData.waiting_elem_for_change)
    elif user_answer == "удалить позицию":
        if current_stage == 1:
            await message.answer(
                "Какую позицию вы хотите удалить?", reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(ChangingData.delete)
    elif user_answer == "добавить позицию":
        if current_stage == 1:
            await message.answer(
                "Напишите название позиций, которые хотите отслеживать",
                reply_markup=ReplyKeyboardRemove(),
            )
            await state.set_state(ChangingData.add)
    elif user_answer == "начать заполнение заново":
        if current_stage == 1:
            await message.answer(
                constants.ASK_LIST_INGREDIENTS, reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(States.waiting_ingredient_list)
    elif user_answer == "отменить":
        if current_stage == 1:
            await message.answer(
                logic.render_list(ingredient_list), reply_markup=buttons_yes_or_not()
            )
            await state.set_state(States.waiting_for_data_confirmation)
    else:
        await message.answer(
            "Пожалуйста, выберите и напишите одно действие:\n•Поменять позицию\n•Удалить позицию\n•Добавить позицию\n•Начать заполнение заново",
            reply_markup=buttons_choose_action(),
        )


@router_changing.message(ChangingData.waiting_elem_for_change)
async def get_answer_about_change(message: Message, state: FSMContext):
    ingredient_for_change = message.text.lower()
    data = await state.update_data()
    changing_list = data.get("ingredient_list")
    if ingredient_for_change == "отмена":
        await message.answer(
            logic.render_list(changing_list), reply_markup=buttons_yes_or_not()
        )
        await state.set_state(States.waiting_for_data_confirmation)
    elif ingredient_for_change not in changing_list:
        await message.answer(
            f'Такой позиции не существует\nПожалуйста, выбери какую позицию ты хочешь изменить:\n•{"\n•".join(changing_list)}',
            reply_markup=button_generator(changing_list),
        )
    elif ingredient_for_change in changing_list:
        await state.update_data(ifc=ingredient_for_change)
        await state.set_state(ChangingData.change)
        await message.answer(
            "Введите новое название для позиции", reply_markup=ReplyKeyboardRemove()
        )


@router_changing.message(ChangingData.change)
async def change(message: Message, state: FSMContext):
    new_ingredient_name = message.text.lower()
    data = await state.get_data()

    ingredient_list = data.get("ingredient_list")
    ingredient_for_change = data.get("ifc")

    if new_ingredient_name == "отмена":
        await state.set_state(States.waiting_for_data_confirmation)
        await message.answer(
            logic.render_list(ingredient_list), reply_markup=buttons_yes_or_not()
        )
    else:
        index = ingredient_list.index(ingredient_for_change)
        ingredient_list[index] = new_ingredient_name
        await state.update_data(ingredient_list=ingredient_list)
        await message.answer(logic.render_list(ingredient_list))
        await state.set_state(States.waiting_for_data_confirmation)
