'''from aiogram import Router
from sqlalchemy.orm import mapped_as_dataclass
from sqlalchemy.orm.base import state_str

import constants
from bot.handlers.buttons import butt, yes_no, otmena
from core import logic
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.states_fsm import States

router_changing = Router()

@router_changing.message(States.change)
async def get_ingred_for_change(mess: Message, state: FSMContext):
    ans = mess.text.lower()
    data = await state.get_data()

    current_stage = data.get('survey_stage')
    compos = data.get('composition')
    current_ing = data.get('current_ing')
    if current_stage == 1:
        ingredient_list = data.get('ingredient_list')
    elif current_stage == 2:
        ingredient_list =compos[current_ing]

    if ans in ingredient_list:
        await state.update_data(ingredient_for_change=ans)
        await state.set_state(States.change_two)
        if current_stage == 1:
            await mess.answer(f'Введи новое название для позиции "{ans}"', reply_markup=ReplyKeyboardRemove())
        elif current_stage == 2:
            await mess.answer(f'Введи новое название для товара "{ans}"', reply_markup=ReplyKeyboardRemove())
    elif ans == 'отмена':
        await state.set_state(States.waiting_check_correct_list_ingredient)
        if current_stage == 1:
            await mess.answer(logic.correct_output_ingredient_list(data['ingredient_list']),
                              reply_markup=yes_no())
        elif current_stage == 2:
            await mess.answer(logic.correct_output_position_list(compos),
                              reply_markup=yes_no())
    else:
        if current_stage == 1:
            await mess.answer(f'Ты не вводил такую позицию\nПожалуйста, введи позицию, которую хотел бы поменять из этого списка:\n{constants.SEPARATOR}\n{"\n".join(ingredient_list)}',
                              reply_markup=butt(ingredient_list))
        elif current_stage == 2:
            await mess.answer(
                f'Ты не вводил такой товар\nПожалуйста, введи товар, который хотел бы поменять из этого списка:\n{constants.SEPARATOR}\n{"\n".join(ingredient_list)}',
                reply_markup=butt(ingredient_list))




@router_changing.message(States.change_two)
async def change(mess:Message, state: FSMContext):
    ans = mess.text.lower()
    data = await state.get_data()

    current_stage = data.get('survey_stage')
    compos = data.get('composition')
    current_ing = data.get('current_ing')

    if ans == 'отмена':
        await state.set_state(States.waiting_check_correct_list_ingredient)
        if current_stage == 1:
            await mess.answer(logic.correct_output_ingredient_list(data['ingredient_list']),
                          reply_markup=yes_no())
        elif current_stage == 2:
            await mess.answer(logic.correct_output_position_list(compos),
                              reply_markup=yes_no())
    if current_stage == 1:
        ingred_for_change = data.get("ingredient_for_change")
        ingred_list = data.get('ingredient_list')
    elif current_stage == 2:
        ingred_for_change = data.get("ingredient_for_change")
        ingred_list = compos[current_ing]

    index = ingred_list.index(ingred_for_change)
    ingred_list[index] = ans
    await state.update_data(ingredient_list=ingred_list)
    if current_stage == 1:
        await mess.answer(logic.correct_output_ingredient_list(ingred_list),
                          reply_markup=yes_no())
    elif current_stage == 2:
        await mess.answer(logic.correct_output_position_list(compos),
                          reply_markup=yes_no())
    await state.set_state(States.waiting_check_correct_list_ingredient)

@router_changing.message(States.delete)
async def get_position_for_delete(mess: Message, state:FSMContext):
    answer = mess.text.lower()
    data = await state.get_data()
    current_stage = data.get('survey_stage')
    compos = data.get('composition')
    current_ing = data.get('current_ing')
    if current_stage == 1:
        ingred_list = data.get('ingredient_list')
    elif current_stage == 2:
        ingred_list = compos[current_ing]
    if answer in ingred_list:
        ingred_list.remove(answer)
        if current_stage == 1:
            await state.update_data(ingredient_list=ingred_list)
            await mess.answer(logic.correct_output_ingredient_list(ingred_list),
                              reply_markup=yes_no())
        elif current_stage == 2:
            await state.update_data(position_list=ingred_list)
            await mess.answer(logic.correct_output_position_list(compos),
                              reply_markup=yes_no())
        await state.set_state(States.waiting_check_correct_list_ingredient)
    elif answer == 'отмена':
        data = await state.get_data()

        await state.set_state(States.waiting_check_correct_list_ingredient)
        if current_stage == 1:
            await mess.answer(logic.correct_output_ingredient_list(data['ingredient_list']),
                              reply_markup=yes_no())
        elif current_stage == 2:
            await mess.answer(logic.correct_output_position_list(compos),
                              reply_markup=yes_no())
    else:
        if current_stage == 1:
            await mess.answer(f'продукта "{answer}" нет в списке\nВыбери что ты хочешь удалить из списка ниже:\n{"\n".join(ingred_list)}',
                              reply_markup=butt(ingred_list))
        elif current_stage == 2:
            await mess.answer(
                f'товара "{answer}" нет в списке\nВыбери что ты хочешь удалить из списка ниже:\n{"\n".join(compos[current_ing])}',
                reply_markup=butt(ingred_list))

@router_changing.message(States.add)
async def add(mess: Message, state: FSMContext):
    answer = logic.convert_string_to_list(mess.text)
    data = await state.get_data()

    current_stage = data.get('survey_stage')
    compos = data.get('composition')
    current_ing = data.get('current_ing')

    if current_stage == 1:
        ingred_list = data.get('ingredient_list')
    elif current_stage == 2:
        ingred_list = compos[current_ing]

    ingred_list.extend(answer)
    if current_stage == 1:
        await mess.answer(logic.correct_output_ingredient_list(ingred_list),
                          reply_markup=yes_no())
    elif current_stage == 2:
        await mess.answer(logic.correct_output_position_list(compos),
                          reply_markup=yes_no())
    await state.set_state(States.waiting_check_correct_list_ingredient)

'''

