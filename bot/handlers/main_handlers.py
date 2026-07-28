from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, reply_markup_union
from aiogram.filters import Command

import constants
from bot.handlers.buttons import (
    buttons_show_delete,
    buttons_yes_or_not,
    buttons_choose_action,
    button_generator,
)
from bot.states_fsm import States, DeleteFromDB, ChangingData
from core import logic
from database import queries

main_router = Router()


@main_router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    user = message.from_user

    if await queries.get_user_data(user.id) is None:
        await state.update_data(ingredient_list=[])  # список отслеживаемых ингредиентов
        await state.update_data(survey_stage=1)  # текущий этап заполнения данных
        await state.update_data(
            composition={}
        )  # ключ-ингридиент, значение-список товаров, куда идет ингр.        await state.update_data(recipes={})#кл-товар, зн:кл-ингридиент, зн-количество игрид.
        await state.update_data(recipes={})
        await state.update_data(position_is_ingredient=[])
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
        await message.answer(
            'Хотите отобразить данные или удалить?"', reply_markup=buttons_show_delete()
        )


@main_router.message(DeleteFromDB.waiting_ans_about_delete_data_from_db)
async def delete_data(message: Message, state: FSMContext):
    answer = message.text.lower()
    if answer == "да":
        user = message.from_user
        await queries.delete_user(user.id)
        await message.answer("Данные удалены", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer(
            "Отменяю операцию по удалению данных", reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state()


@main_router.message(States.waiting_ingredient_list)
async def get_list_ingredients(message: Message, state: FSMContext):
    user_answer = message.text
    result_user_input = logic.convert_string_to_list(user_answer)
    await state.update_data(ingredient_list=result_user_input)

    await message.answer(
        text=logic.render_list(result_user_input), reply_markup=buttons_yes_or_not()
    )
    await state.set_state(States.waiting_for_data_confirmation)


@main_router.message(States.waiting_for_data_confirmation)
async def check_correctness_data(message: Message, state: FSMContext):
    user_answer = message.text.lower()
    data = await state.get_data()

    current_survey_stage = data.get("survey_stage")

    if user_answer == "да" and current_survey_stage == 1:
        await message.answer(
            constants.ASK_LIST_POSITIONS.format(ingredient=data["ingredient_list"][0]),
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(States.waiting_position_list)

    elif user_answer == "да" and current_survey_stage == 2:
        recipes = data.get("recipes")
        composition = data.get("composition")
        for ingr, p_l in composition.items():
            for p in p_l:
                recipes.setdefault(p, {})
                recipes[p].setdefault(ingr, 0)
        await state.update_data(recipes=recipes)

        first_pos = list(recipes.keys())[0]
        first_ingred = list(recipes[first_pos].keys())[0]
        await message.answer(
            f'Сколько ингридиента "{first_ingred}" идет в товар "{first_pos}"?\n Пожалуйста, укажите в ГРАММАХ',
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(States.waiting_quantity)
    elif user_answer == "да" and current_survey_stage == 3:
        await state.set_state(States.waiting_save_confirmation)
        await message.answer(
            f"Подтвердите сохранение данных", reply_markup=buttons_yes_or_not()
        )
    elif user_answer == "нет":
        if current_survey_stage == 1:
            await message.answer(
                f"Что вы хотите изменить?\n{constants.SEPARATOR}\nВыберите и напишите одно действие:{constants.CHOOSING_ACTION}",
                reply_markup=buttons_choose_action(),
            )
            await state.set_state(ChangingData.waiting_result_choosing_action)
        elif current_survey_stage == 2:
            composition = data.get("composition")
            await message.answer(
                f"В какой позиции вы хотите внести изменения?",
                reply_markup=button_generator(list(composition.keys())),
            )
            await state.set_state(ChangingData.waiting_ingredient_name)
        elif current_survey_stage == 3:
            recipes = data.get("recipes")
            await message.answer(
                f"В каком товаре вы хотите внести изменения?",
                reply_markup=button_generator(list(recipes.keys())),
            )
            await state.set_state(ChangingData.waiting_position_name_for_change)
    else:
        await message.answer('Я не понимаю\nПожалуйста, введите "да" или "нет"')


@main_router.message(States.waiting_position_list)
async def get_position_list(message: Message, state: FSMContext):
    user_answer = logic.convert_string_to_list(message.text)

    data = await state.get_data()
    composition = data.get("composition")
    count = data.get("count", 0)
    ingredient_list = data.get("ingredient_list")
    position_is_ingredient = data.get("position_is_ingredient")

    if ingredient_list[count] == user_answer[0]:
        position_is_ingredient.append(user_answer[0])
        await state.update_data(position_is_ingredient=position_is_ingredient)
    else:
        composition.setdefault(ingredient_list[count], user_answer)
    count += 1
    await state.update_data(composition=composition)
    await state.update_data(count_ingred=0)
    await state.update_data(count_pos=0)

    if (
        count < len(ingredient_list)
        and ingredient_list[count] not in position_is_ingredient
    ):
        await message.answer(
            constants.ASK_LIST_POSITIONS.format(ingredient=ingredient_list[count])
        )
        await state.update_data(count=count)
    else:
        await state.update_data(survey_stage=2)
        for elem in position_is_ingredient:
            ingredient_list.remove(elem)
        await state.update_data(ingredient_list=ingredient_list)
        await message.answer(
            logic.render_dict(composition, list_for_add=position_is_ingredient),
            reply_markup=buttons_yes_or_not(),
        )
        await state.set_state(States.waiting_for_data_confirmation)


@main_router.message(States.waiting_quantity)
async def get_quantity(message: Message, state: FSMContext):
    quantity = message.text
    data = await state.get_data()
    recipes = data.get("recipes")
    count_ingred = data.get("count_ingred")
    count_pos = data.get("count_pos")

    cpl = list(recipes.keys())  # current_position_list
    cil = list(recipes[cpl[count_pos]].keys())  # current_ingredient_list

    if quantity.isdigit():
        recipes[cpl[count_pos]][cil[count_ingred]] = quantity
        await state.update_data(recipes=recipes)
    else:
        await message.answer(
            f'Некорректный ввод\nСколько ингридиента "{cil[count_ingred]}" идет в товар "{cpl[count_pos]}"?\n Пожалуйста, укажите в ГРАММАХ'
        )

    count_ingred += 1

    if count_ingred < len(cil):
        await state.update_data(count_ingred=count_ingred)
        await message.answer(
            f'Сколько ингридиента "{cil[count_ingred]}" идет в товар "{cpl[count_pos]}"?\n Пожалуйста, укажите в ГРАММАХ'
        )
    else:
        if count_pos < len(cpl) - 1:
            count_pos += 1
            count_ingred = 0
            current_pos_list = list(recipes.keys())
            current_pos = current_pos_list[count_pos]
            current_ingred_list = list(recipes[current_pos].keys())
            current_ingred = current_ingred_list[count_ingred]
            await state.update_data(count_pos=count_pos)
            await state.update_data(count_ingred=count_ingred)
            await message.answer(
                f'Сколько ингридиента "{current_ingred}" идет в товар "{current_pos}"?\n Пожалуйста, укажите в ГРАММАХ'
            )
        else:
            await state.update_data(survey_stage=3)
            await message.answer(
                constants.CHECKING_CORRECT_DATA.format(
                    sep=constants.SEPARATOR, checking_data=logic.show_recipes(recipes)
                ),
                reply_markup=buttons_yes_or_not(),
            )
            await state.set_state(States.waiting_for_data_confirmation)


@main_router.message(States.waiting_save_confirmation)
async def saving_data(message: Message, state: FSMContext):
    answer = message.text.lower()
    user_id = message.from_user.id
    data = await state.get_data()
    recipes = data.get("recipes")
    if answer == "да":
        position_is_ingredient = data.get("position_is_ingredient")
        for pos in position_is_ingredient:
            recipes.setdefault(pos, {})
            recipes[pos][pos] = 1
        await state.update_data(recipes=recipes)
        await queries.add_new_user(user_id, recipes)
        await message.answer(
            f"Сохранены следующие данные:\n{logic.show_recipes(recipes)}"
        )
        await state.clear()
    else:
        await message.answer(
            constants.CHECKING_CORRECT_DATA.format(
                sep=constants.SEPARATOR, checking_data=logic.show_recipes(recipes)
            ),
            reply_markup=buttons_yes_or_not(),
        )
        await state.set_state(States.waiting_for_data_confirmation)
