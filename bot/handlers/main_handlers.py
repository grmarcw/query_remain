from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

import constants
from bot.handlers.buttons import buttons_show_delete, buttons_yes_or_not, buttons_choose_action
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
        await state.update_data(composition={})#ключ-ингридиент, значение-список товаров, куда идет ингр.
        await state.update_data(count=0)
        await state.update_data(recipes={})#кл-товар, зн:кл-ингридиент, зн-количество игрид.

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
    elif user_answer == 'нет':
        await message.answer(f'Что вы хотите изменить?\n{constants.SEPARATOR}\nВыберите и напишите одно действие:\n{constants.SEPARATOR}\n•Поменять позицию\n•Удалить позицию\n•Добавить позицию\n•Начать заполнение заново',
                             reply_markup=buttons_choose_action())
        await state.set_state(ChangingData.waiting_result_choosing_action)

    else:
        await message.answer('Я не понимаю\nПожалуйста, введите "да" или "нет"')
