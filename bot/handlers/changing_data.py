from itertools import count

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.dialects import mssql

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

    composition = data.get('composition')
    cifc = data.get('cifc')

    if user_answer == "поменять позицию":
        if current_stage == 1:
            await message.answer(
                "Какую позицию вы хотите изменить?", reply_markup=button_generator(ingredient_list)
            )
            await state.set_state(ChangingData.waiting_elem_for_change)
        elif current_stage == 2:
            await message.answer(
                "Какой товар вы хотите изменить?", reply_markup=button_generator(composition[cifc])
            )
            await state.set_state(ChangingData.waiting_elem_for_change)

    elif user_answer == "удалить позицию":
        if current_stage == 1:
            await state.set_state(ChangingData.delete)
            await message.answer(
                "Какую позицию вы хотите удалить?", reply_markup=button_generator(ingredient_list)
            )
        elif current_stage == 2:
            await state.set_state(ChangingData.delete)
            await message.answer(
                "Какой товар вы хотите удалить?", reply_markup=button_generator(composition[cifc])
            )

    elif user_answer == "добавить позицию":
        if current_stage == 1:
            await state.set_state(ChangingData.add)
            await message.answer(
                "Напишите названия позиций, которые хотите отслеживать",
                reply_markup=ReplyKeyboardRemove(),
            )
        elif current_stage == 2:
            await state.set_state(ChangingData.add)
            await message.answer(
                "Напишите названия товаров, которые хотите добавить",
                reply_markup=ReplyKeyboardRemove(),
            )

    elif user_answer == "начать заполнение заново":
        if current_stage == 1:
            await message.answer(
                constants.ASK_LIST_INGREDIENTS, reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(States.waiting_ingredient_list)
        elif current_stage == 2:
            await message.answer(constants.ASK_LIST_POSITIONS.format(ingredient=cifc),
                                 reply_markup=ReplyKeyboardRemove())
            await state.set_state(ChangingData.recomposition)

    elif user_answer == "отменить":
        await state.set_state(States.waiting_for_data_confirmation)
        if current_stage == 1:
            await message.answer(
                logic.render_list(ingredient_list), reply_markup=buttons_yes_or_not()
            )
        elif current_stage == 2:
            await state.set_state(States.waiting_for_data_confirmation)
            await message.answer(logic.render_dict(composition), reply_markup=buttons_yes_or_not())
    else:
        await message.answer(
            "Пожалуйста, выберите и напишите одно действие:\n•Поменять позицию\n•Удалить позицию\n•Добавить позицию\n•Начать заполнение заново",
            reply_markup=buttons_choose_action(),
        )


@router_changing.message(ChangingData.waiting_elem_for_change)
async def get_answer_about_change(message: Message, state: FSMContext):
    position_for_change = message.text.lower()
    data = await state.update_data()
    changing_list = data.get("ingredient_list")
    cifc = data.get('cifc')
    current_stage = data.get("survey_stage")
    composition = data.get('composition')
    if current_stage == 1:
        changing_list = data.get("ingredient_list")
    elif current_stage == 2:
        changing_list = composition[cifc]

    if position_for_change == "отмена":
        await state.set_state(States.waiting_for_data_confirmation)
        if current_stage == 1:
            await message.answer(
                logic.render_list(changing_list), reply_markup=buttons_yes_or_not()
            )
        elif current_stage == 2:
            await message.answer(logic.render_dict(composition), reply_markup=buttons_yes_or_not())
    elif position_for_change not in changing_list:
        await message.answer(
            f'Такой позиции не существует\nПожалуйста, выбери какую позицию ты хочешь изменить:\n•{"\n•".join(changing_list)}',
            reply_markup=button_generator(changing_list),
        )
    elif position_for_change in changing_list:
        if current_stage == 1:
            await state.update_data(ifc=position_for_change)
        elif current_stage == 2:
            await state.update_data(pfc=position_for_change)
        await state.set_state(ChangingData.change)
        await message.answer(
            "Введите новое название для позиции", reply_markup=ReplyKeyboardRemove()
        )


@router_changing.message(ChangingData.change)
async def change(message: Message, state: FSMContext):
    new_ingredient_name = message.text.lower()
    data = await state.get_data()
    current_stage = data.get("survey_stage")

    composition = data.get('composition')
    cifc = data.get('cifc')
    position_for_change = data.get('pfc')

    ingredient_list = data.get("ingredient_list")
    ingredient_for_change = data.get("ifc")


    if current_stage == 1:
        list_for_change = ingredient_list
        element_for_change = ingredient_for_change
    elif current_stage == 2:
        list_for_change = composition[cifc]
        element_for_change = position_for_change
    if new_ingredient_name == "отмена":
        await state.set_state(States.waiting_for_data_confirmation)
        if current_stage == 1:
            await message.answer(
                logic.render_list(ingredient_list), reply_markup=buttons_yes_or_not()
            )
        elif current_stage == 2:
            await message.answer(
                logic.render_dict(composition), reply_markup=buttons_yes_or_not()
            )
    else:
        index = list_for_change.index(element_for_change)
        list_for_change[index] = new_ingredient_name
        if current_stage == 1:
            await state.update_data(ingredient_list=list_for_change)
            await message.answer(logic.render_list(list_for_change),
                                 reply_markup=buttons_yes_or_not())
        elif current_stage == 2:
            await state.update_data(composition=composition)
            await message.answer(logic.render_dict(composition),
                                 reply_markup=buttons_yes_or_not())
        await state.set_state(States.waiting_for_data_confirmation)


@router_changing.message(ChangingData.delete)
async def delete(message: Message, state:FSMContext):
    position_for_delete = message.text.lower()
    data = await state.get_data()
    current_stage = data.get("survey_stage")
    ingredient_list = data.get('ingredient_list')

    composition = data.get('composition')
    cifc = data.get('cifc')
    if current_stage == 1:
        list_for_delete = ingredient_list
    elif current_stage == 2:
        list_for_delete = composition[cifc]
    if position_for_delete == 'отмена':
        await state.set_state(States.waiting_for_data_confirmation)
        if current_stage == 1:
            await message.answer(logic.render_list(ingredient_list),
                                 reply_markup=buttons_yes_or_not())
        elif current_stage == 2:
            await message.answer(logic.render_dict(composition),
                                 reply_markup=buttons_yes_or_not())
    elif position_for_delete in list_for_delete:
        list_for_delete.remove(position_for_delete)
        await state.set_state(States.waiting_for_data_confirmation)
        if current_stage == 1:
            await state.update_data(ingredient_list=ingredient_list)
            await message.answer(f'Позиция "{position_for_delete}" удалена из списка отслеживаемых продуктов')
            await message.answer(logic.render_list(ingredient_list),
                                 reply_markup=buttons_yes_or_not())
        elif current_stage == 2:
            await state.update_data(composition=composition)
            await message.answer(f'Товар "{position_for_delete}" удален')
            await message.answer(logic.render_dict(composition),
                                 reply_markup=buttons_yes_or_not())

    else:
        await message.answer(f'продукта "{position_for_delete}" нет в списке\nВыбери что ты хочешь удалить из списка ниже:\n•{"\n•".join(list_for_delete)}',
                              reply_markup=button_generator(list_for_delete))

@router_changing.message(ChangingData.add)
async def add(message: Message, state: FSMContext):
    new_positions = logic.convert_string_to_list(message.text)
    data = await state.get_data()
    current_stage = data.get('survey_stage')
    composition = data.get('composition')
    cifc = data.get('cifc')

    ingredient_list = data.get('ingredient_list')
    if current_stage == 1:
        ingredient_list.extend(new_positions)
        await state.update_data(ingredient_list=ingredient_list)
        await message.answer(logic.render_list(ingredient_list),
                             reply_markup=buttons_yes_or_not())
    elif current_stage == 2:
        composition[cifc].extend(new_positions)
        await state.update_data(composition=composition)
        await message.answer(logic.render_dict(composition),
                             reply_markup=buttons_yes_or_not())
    else:
        await message.answer(str(current_stage))

    await state.set_state(States.waiting_for_data_confirmation)

@router_changing.message(ChangingData.waiting_ingredient_name)
async def choose_composition_for_change(message: Message, state: FSMContext):
    ingredient_name = message.text.lower()
    data = await state.get_data()

    composition = data.get('composition')
    ingredient_list = data.get('ingredient_list')

    if ingredient_name == 'отмена':
        await message.answer(logic.render_dict(composition),
                             reply_markup=buttons_yes_or_not())
        await state.set_state(States.waiting_for_data_confirmation)
    elif ingredient_name not in list(composition.keys()):
        await message.answer(
            f'Нет такой позиции\nПожалуйста введи позицию, в которой хочешь внести изменения:\n{constants.SEPARATOR}\n{logic.render_dict(composition,option=2)}',
        reply_markup=button_generator(ingredient_list)
        )
    else:
        await state.update_data(cifc=ingredient_name)#cifc-current ingredient for change
        await state.update_data(currect_position_list=composition[ingredient_name])
        await state.set_state(ChangingData.waiting_result_choosing_action)
        await message.answer(f'Что вы хотите изменить?\n{constants.SEPARATOR}\nВыберите и напишите одно действие:\n{constants.SEPARATOR}\n•Поменять позицию\n•Удалить позицию\n•Добавить позицию\n•Начать заполнение заново',
                             reply_markup=buttons_choose_action())


@router_changing.message(ChangingData.recomposition)
async def recomposite(message: Message, state: FSMContext):
    position_list = logic.convert_string_to_list(message.text)
    data = await state.get_data()
    composition = data.get('composition')
    cifc = data.get('cifc')

    composition[cifc] = position_list
    await state.update_data(composition=composition)
    await state.set_state(States.waiting_for_data_confirmation)
    await message.answer(logic.render_dict(composition), reply_markup=buttons_yes_or_not())

