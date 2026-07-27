from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, reply_markup_union
from aiogram.filters import Command

import constants
from bot.handlers.buttons import buttons_show_delete, buttons_yes_or_not, buttons_choose_action, button_generator
from bot.states_fsm import States, DeleteFromDB, ChangingData
from core import logic
from database import queries

main_router = Router()


@main_router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    user = message.from_user

    if await queries.get_user_data(user.id) is None:
        await state.update_data(ingredient_list=[])#список отслеживаемых ингредиентов
        await state.update_data(survey_stage=1)#текущий этап заполнения данных
        await state.update_data(composition={})#ключ-ингридиент, значение-список товаров, куда идет ингр.        await state.update_data(recipes={})#кл-товар, зн:кл-ингридиент, зн-количество игрид.
        await state.update_data(recipes={})
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

@main_router.message(States.waiting_ingredient_list)
async def get_list_ingredients(message: Message, state: FSMContext):
    user_answer = message.text
    result_user_input = logic.convert_string_to_list(user_answer)
    await state.update_data(ingredient_list=result_user_input)


    await message.answer(text=logic.render_list(result_user_input),
                         reply_markup=buttons_yes_or_not())
    await state.set_state(States.waiting_for_data_confirmation)


@main_router.message(States.waiting_for_data_confirmation)
async def check_correctness_data(message: Message, state: FSMContext):
    user_answer = message.text.lower()
    data = await state.get_data()

    current_survey_stage = data.get('survey_stage')

    if user_answer == 'да' and current_survey_stage == 1:
        await message.answer(constants.ASK_LIST_POSITIONS.format(ingredient=data['ingredient_list'][0]),
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(States.waiting_position_list)

    elif user_answer == 'да' and current_survey_stage == 2:
        pass

    elif user_answer == 'нет':
        if current_survey_stage == 1:
            await message.answer(f'Что вы хотите изменить?\n{constants.SEPARATOR}\nВыберите и напишите одно действие:\n{constants.SEPARATOR}\n•Поменять позицию\n•Удалить позицию\n•Добавить позицию\n•Начать заполнение заново',
                                 reply_markup=buttons_choose_action())
            await state.set_state(ChangingData.waiting_result_choosing_action)
        elif current_survey_stage == 2:
            await message.answer(f'В какой позиции вы хотите внести изменения?',
                                 reply_markup=button_generator(data.get('ingredient_list')))
            await state.set_state(ChangingData.waiting_ingredient_name)
    else:
        await message.answer('Я не понимаю\nПожалуйста, введите "да" или "нет"')

@main_router.message(States.waiting_position_list)
async def get_position_list(message: Message, state: FSMContext):
    user_answer = logic.convert_string_to_list(message.text)

    data = await state.get_data()
    composition = data.get('composition')
    count = data.get('count', 0)
    ingredient_list = data.get('ingredient_list')

    composition.setdefault(ingredient_list[count], user_answer)
    count += 1
    await state.update_data(composition=composition)
    await state.update_data(count_ingred=0)
    await state.update_data(count_pos=0)

    if count < len(ingredient_list):
        await message.answer(constants.ASK_LIST_POSITIONS.format(ingredient=ingredient_list[count]))
        await state.update_data(count=count)
    else:
        recipes = data.get('recipes')
        for ingr, p_l in composition.items():
            for p in p_l:
                recipes.setdefault(p,{})
                recipes[p].setdefault(ingr, 0)
        await state.update_data(recipes=recipes)
        await state.update_data(survey_stage=2)
        await message.answer(logic.render_dict(composition),
                          reply_markup=buttons_yes_or_not())
        await state.set_state(States.waiting_for_data_confirmation)
