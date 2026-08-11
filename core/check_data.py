from aiogram.types import ReplyKeyboardRemove

import constants
from bot.buttons import button_generator, buttons_yes_or_not, buttons_show_delete
from bot.states_fsm import (
    States,
    ChangingData,
    FillingStates,
    CurrentActualBalance,
    Main,
)
import constants
from constants import general, stage_11, stage_14, stage_13, stage_15
from core import renderers, import_loader
from database import queries
from database.models import SecondaryData


async def check_data_in_db(instance):
    data = await queries.get_user_data(instance.user_id)
    data_from_second_db = await queries.get_user_data(instance.user_id, SecondaryData)
    if data is None:
        instance.survey_stage = 1
        message_answer = import_loader.get_constants(instance.survey_stage).ASK_LIST
        buttons = ReplyKeyboardRemove()
        next_state = FillingStates.waiting_for_data_list
    elif data is not None:
        if data.deliveries is None:
            instance.survey_stage = 5
            instance.current_data_list = []
            instance.positions_products = []
            for recipe in data.recipes.values():
                for ingredient in recipe.keys():
                    if ingredient not in instance.data_list:
                        instance.data_list.append(ingredient)
            if data.positions_products:
                instance.data_list.extend(data.positions_products)
            message_answer = import_loader.get_constants(instance.survey_stage).ASK_LIST
            buttons = ReplyKeyboardRemove()
            next_state = FillingStates.waiting_for_data_list

        else:
            if data_from_second_db is None:
                instance.survey_stage = 7
                instance.count = 0
                for recipe in data.recipes.values():
                    for ingredient in recipe.keys():
                        if ingredient not in instance.data_list:
                            instance.data_list.append(ingredient)
                if data.positions_products:
                    instance.data_list.extend(data.positions_products)
                    message_answer = constants.stage_7.ASK_QUANTITY.format(
                        position=instance.data_list[instance.count]
                    )
                    buttons = ReplyKeyboardRemove()
                    next_state = CurrentActualBalance.waiting_for_quantity
            else:
                message_answer = f"Все первичные данные заполнены"
                buttons = button_generator(["/input_daily_data"], without_cancel=True)
                next_state = States.clear

    return (message_answer, buttons, next_state)


def check_correctness_data(user_answer: str, instance):
    stage = instance.survey_stage
    const = import_loader.get_constants(stage)
    try:
        const_plus_one = import_loader.get_constants(stage + 1)
    except ModuleNotFoundError:
        const_plus_one = const

    if user_answer == "да":
        if stage == 1:
            instance.data_list = instance.current_data_list
            instance.data_list_copy = instance.data_list.copy()
            instance.current_data_list = []
            instance.current_data = instance.current_data_list

            instance.survey_stage = 2

            message_answer = const_plus_one.ASK_LIST
            buttons = button_generator(
                instance.data_list, ["готово"], without_cancel=True
            )
            next_state = FillingStates.waiting_for_products_list
        elif stage == 2:
            instance.positions_products = instance.current_data_list.copy()
            instance.current_data_list = []
            instance.data_list_copy = instance.current_data_list.copy()
            instance.current_data = instance.data_dict

            instance.survey_stage = 3

            message_answer = const_plus_one.ASK_LIST.format(
                ingredient=instance.data_list[0]
            )
            buttons = ReplyKeyboardRemove()
            next_state = FillingStates.waiting_for_data_for_composition

        elif stage == 3:
            instance.current_position_for_change = list(instance.data_dict.keys())[0]
            instance.current_data_list = instance.data_dict[
                instance.current_position_for_change
            ]
            instance.current_data = instance.recipes
            instance.count = 0

            instance.survey_stage = 4

            message_answer = const_plus_one.ASK_QUANTITY.format(
                position=instance.current_position_for_change,
                product=instance.current_data_list[instance.count],
            )
            buttons = ReplyKeyboardRemove()
            next_state = FillingStates.waiting_quantity

        elif stage == 4:
            instance.data_dict = instance.data_dict_copy.copy()
            instance.data_list = instance.data_list_copy.copy()
            instance.count = 0
            instance.current_data = instance.recipes

            message_answer = general.FILLED_RECIPES_DATA + general.CONFIRM_SAVING
            buttons = buttons_yes_or_not()
            next_state = States.waiting_save_confirmation
        elif stage == 5:
            for deliverier in instance.current_data_list:
                instance.data_dict.setdefault(deliverier, [])

            instance.survey_stage = 6
            instance.count = 0
            instance.current_data = instance.recipes
            instance.current_position_for_change = instance.data_list[instance.count]
            instance.current_data_list = []

            message_answer = const_plus_one.ASK_LIST.format(
                position=instance.current_position_for_change
            )
            buttons = button_generator(
                list(instance.data_dict.keys()), without_cancel=True
            )
            next_state = FillingStates.waiting_for_delivery_data_composition
        elif stage == 6:
            if instance.count == 67:  # если пользователь хочет заполнить данные заново
                instance.data_dict = {}
                for deliverier in instance.current_data_list:
                    instance.data_dict.setdefault(deliverier, [])

                instance.count = 0
                instance.current_data = instance.data_dict
                instance.current_position_for_change = instance.data_list[
                    instance.count
                ]

                message_answer = const_plus_one.ASK_LIST.format(
                    position=instance.current_position_for_change
                )
                buttons = button_generator(
                    list(instance.data_dict.keys()), without_cancel=True
                )
                next_state = FillingStates.waiting_for_delivery_data_composition
            else:
                message_answer = general.FILLED_DELIVERY_DATA + general.CONFIRM_SAVING
                buttons = buttons_yes_or_not()
                next_state = States.waiting_save_confirmation

        elif stage == 7:
            message_answer = general.FILLED_BALANCE_DATA + general.CONFIRM_SAVING
            buttons = buttons_yes_or_not()
            next_state = States.waiting_save_confirmation
        elif stage == 8:
            instance.dict_in_dict["date"] = instance.date
            instance.dict_in_dict["sold"] = instance.data_dict
            instance.current_data_list = []
            instance.current_data = instance.current_data_list
            instance.data_list = list(instance.deliveries.keys())
            instance.data_list_copy = instance.data_list.copy()

            instance.survey_stage = 9

            message_answer = const_plus_one.ASK_LIST
            buttons = button_generator(
                instance.data_list, ["готово"], without_cancel=True
            )
            next_state = Main.waiting_for_deliveries_names

        elif stage == 9:
            if instance.current_data_list == []:
                instance.dict_in_dict["delivery"] = {}
                instance.survey_stage = 11
                instance.data_list = instance.positions.copy()
                instance.data_list_copy = instance.data_list.copy()
                instance.current_data_list = []
                instance.current_data = instance.current_data_list

                return (
                    stage_11.ASK_LIST,
                    button_generator(
                        instance.data_list, ["готово"], without_cancel=True
                    ),
                    FillingStates.waiting_for_products_list,
                )

            else:
                instance.survey_stage = 10

                instance.count = 0
                instance.data_dict = {}
                instance.data_list = instance.current_data_list.copy()
                instance.data_dict = {}
                for deliverier, positions in instance.deliveries.items():
                    if deliverier in instance.current_data_list:
                        instance.data_dict.setdefault(deliverier, positions)

                instance.current_position_for_change = list(instance.data_dict.keys())[
                    instance.count
                ]
                instance.current_data_list = instance.data_dict[
                    instance.current_position_for_change
                ]
                instance.data_list = list(instance.data_dict.keys())
                instance.current_data = instance.recipes

                message_answer = const_plus_one.ASK_QUANTITY.format(
                    position=instance.current_data_list[instance.count]
                )
                buttons = ReplyKeyboardRemove()
                next_state = FillingStates.waiting_quantity
        elif stage == 10:
            instance.dict_in_dict.setdefault("delivery", {})
            for positions_and_quantity in instance.recipes.values():
                for position, quantity in positions_and_quantity.items():
                    instance.dict_in_dict["delivery"][position] = quantity

            instance.data_list = instance.positions.copy()
            instance.data_list_copy = instance.data_list.copy()
            instance.current_data_list = []
            instance.current_data = instance.current_data_list

            instance.survey_stage = 11

            message_answer = const_plus_one.ASK_LIST
            buttons = button_generator(
                instance.data_list, ["готово"], without_cancel=True
            )
            next_state = FillingStates.waiting_for_products_list
        elif stage == 11:
            if instance.current_data_list == []:
                instance.survey_stage = 13
                instance.dict_in_dict["shipment_from"] = {}

                instance.data_list = instance.positions.copy()
                instance.data_list_copy = instance.data_list.copy()
                instance.current_data_list = []
                instance.current_data = instance.current_data_list

                return (
                    stage_13.ASK_LIST,
                    button_generator(
                        instance.data_list, ["готово"], without_cancel=True
                    ),
                    FillingStates.waiting_for_products_list,
                )

            instance.data_dict = {}
            instance.count = 0
            instance.data_list = instance.current_data_list.copy()

            instance.current_position_for_change = instance.data_list[0]
            instance.current_data = instance.data_dict

            instance.survey_stage = 12

            message_answer = const_plus_one.ASK_QUANTITY.format(
                position=instance.data_list[0]
            )
            buttons = ReplyKeyboardRemove()
            next_state = Main.waiting_for_quantity_sold
        elif stage == 12:
            instance.dict_in_dict["shipment_from"] = instance.data_dict

            instance.data_list = instance.positions.copy()
            instance.data_list_copy = instance.data_list.copy()
            instance.current_data_list = []
            instance.current_data = instance.current_data_list

            instance.survey_stage = 13

            message_answer = const_plus_one.ASK_LIST
            buttons = button_generator(
                instance.data_list, ["готово"], without_cancel=True
            )
            next_state = FillingStates.waiting_for_products_list
        elif stage == 13:
            if instance.current_data_list == []:
                instance.survey_stage = 15
                instance.dict_in_dict["shipment_to"] = {}

                instance.positions_products = sorted(
                    list(set(instance.positions + instance.products))
                )
                instance.data_list = instance.positions_products.copy()

                return (
                    stage_15.ASK_LIST,
                    button_generator(
                        instance.data_list, ["готово"], without_cancel=True
                    ),
                    FillingStates.waiting_for_products_list,
                )
            instance.data_dict = {}
            instance.count = 0

            instance.data_list = instance.current_data_list.copy()

            instance.current_position_for_change = instance.data_list[0]
            instance.current_data = instance.data_dict

            instance.survey_stage = 14
            message_answer = stage_14.ASK_QUANTITY.format(
                position=instance.data_list[0]
            )
            buttons = ReplyKeyboardRemove()
            next_state = Main.waiting_for_quantity_sold
        elif stage == 14:
            instance.dict_in_dict["shipment_to"] = instance.data_dict

            instance.positions_products = sorted(
                list(set(instance.positions + instance.products))
            )
            instance.data_list = instance.positions_products.copy()
            instance.data_list_copy = instance.data_list.copy()
            instance.current_data_list = []
            instance.current_data = instance.current_data_list

            instance.survey_stage = 15

            message_answer = const_plus_one.ASK_LIST
            buttons = button_generator(
                instance.data_list, ["готово"], without_cancel=True
            )
            next_state = FillingStates.waiting_for_products_list
        elif stage == 15:
            pass

    elif user_answer == "нет":
        if stage in (1, 2, 5, 9, 11, 13, 15):
            message_answer = const.ASK_CHOOSING_ACTION + const.CHOOSING_ACTION
            buttons = button_generator(const.CHOOSING_ACTION_LIST)
            next_state = ChangingData.waiting_result_choosing_action
        elif stage in (3, 4, 10):
            message_answer = const.ASK_KEY_FOR_CHANGE
            next_state = ChangingData.waiting_ingredient_name
            if stage == 3:
                instance.current_data_list = []
                buttons = button_generator(list(instance.data_dict.keys()))
            elif stage == 4 or stage == 10:
                instance.current_data_list = []
                instance.data_list_copy = instance.data_list.copy()
                instance.data_dict_copy = instance.data_dict.copy()

                buttons = button_generator(list(instance.recipes.keys()))
        elif stage == 6:
            if instance.count != 67:  # Если запущена проверка корректности данных
                message_answer = const.ASK_KEY_FOR_CHANGE
                buttons = buttons_yes_or_not()
                next_state = None
                instance.count = 67
            else:  # если задан вопрос о повторном заполнении данных
                message_answer = renderers.render_list_or_dict(
                    instance.current_data, stage
                )
                buttons = buttons_yes_or_not()
                next_state = None
                instance.count = 0
        elif stage in (7, 8, 12, 14):
            instance.current_data_list = instance.data_list.copy()
            message_answer = const.ASK_CHOOSING_ACTION + const.CHOOSING_ACTION
            buttons = button_generator(const.CHOOSING_ACTION_LIST)
            next_state = ChangingData.waiting_result_choosing_action

    else:
        message_answer = general.INPUT_YES_NO
        buttons = buttons_yes_or_not()
        next_state = None

    return (message_answer, buttons, next_state)


def choose_action(user_answer, instance):
    user_answer = user_answer.capitalize()
    stage = instance.survey_stage
    const = import_loader.get_constants(stage)
    actions = const.CHOOSING_ACTION_LIST

    if user_answer == "Отменить":
        message_answer = renderers.render_list_or_dict(
            instance.current_data, stage, instance.positions_products
        )
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation
    elif user_answer not in actions:
        message_answer = (
            general.INCORRECT_INPUT + const.ASK_CHOOSING_ACTION + const.CHOOSING_ACTION
        )
        buttons = button_generator(const.CHOOSING_ACTION_LIST)
        next_state = None

    elif user_answer == actions[0]:  # изменить
        if instance.current_data_list == []:
            message_answer = const.EMPTY + renderers.render_list_or_dict(
                instance.current_data, stage, instance.positions_products
            )
            buttons = buttons_yes_or_not()
            next_state = FillingStates.waiting_for_data_confirmation
        else:
            message_answer = const.ASK_NAME_FOR_CHANGE
            buttons = button_generator(instance.current_data_list)
            next_state = ChangingData.waiting_element_for_change

    elif user_answer == actions[1]:  # Удалить
        # для stage_4/stage_7/stage_8/stage_10/stage_12/stage_14 - Начать заполнение заново
        if stage in (1, 2, 3, 5, 6, 9, 11, 13, 15):
            if instance.current_data_list == []:
                message_answer = const.EMPTY + renderers.render_list_or_dict(
                    instance.current_data, stage, instance.positions_products
                )
                buttons = buttons_yes_or_not()
                next_state = FillingStates.waiting_for_data_confirmation
            else:
                message_answer = const.ASK_NAME_FOR_DELETE
                buttons = button_generator(instance.current_data_list)
                next_state = ChangingData.delete
        elif stage == 4:
            current_product = list(instance.recipes.keys())[instance.count]
            positions_list = instance.current_data_list
            instance.data_dict = {}
            instance.data_list = instance.current_data_list.copy()
            for ingredient in positions_list:
                instance.data_dict.setdefault(ingredient, [])
                instance.data_dict[ingredient].append(current_product)

            instance.current_position_for_change = list(instance.data_dict.keys())[0]
            instance.current_data_list = instance.data_dict[
                instance.current_position_for_change
            ]
            instance.count = 0
            return (
                constants.stage_4.ASK_QUANTITY.format(
                    position=instance.current_position_for_change,
                    product=instance.current_data_list[instance.count],
                ),
                ReplyKeyboardRemove(),
                FillingStates.waiting_quantity,
            )
        elif stage == 7:
            instance.count = 0
            instance.data_dict = {}
            return (
                constants.stage_7.ASK_QUANTITY.format(
                    position=instance.data_list[instance.count]
                ),
                ReplyKeyboardRemove(),
                CurrentActualBalance.waiting_for_quantity,
            )
        elif stage == 8:
            instance.count = 0
            instance.data_dict = {}
            return (
                const.ASK_QUANTITY.format(position=instance.data_list[0]),
                ReplyKeyboardRemove(),
                Main.waiting_for_quantity_sold,
            )

        elif stage == 10:
            current_delivery = list(instance.current_data.keys())[instance.count]
            instance.data_dict = {}
            instance.data_list = []
            instance.data_list.append(current_delivery)
            instance.data_dict[current_delivery] = instance.current_data_list
            instance.count = 0

            instance.current_position_for_change = list(instance.data_dict.keys())[
                instance.count
            ]
            instance.current_data_list = instance.data_dict[
                instance.current_position_for_change
            ]

            message_answer = constants.stage_10.ASK_QUANTITY.format(
                position=instance.current_data_list[instance.count]
            )
            buttons = ReplyKeyboardRemove()
            next_state = FillingStates.waiting_quantity

        elif stage in (12, 14):
            instance.data_dict = {}
            instance.count = 0
            instance.data_list = instance.current_data_list.copy()

            instance.current_position_for_change = instance.data_list[0]
            instance.current_data = instance.data_dict

            message_answer = const.ASK_QUANTITY.format(position=instance.data_list[0])
            buttons = ReplyKeyboardRemove()
            next_state = Main.waiting_for_quantity_sold

    elif user_answer == actions[2]:  # Добавить
        if stage in (1, 2, 5):
            message_answer = const.ASK_LIST
        elif stage == 3:
            message_answer = const.ASK_LIST.format(
                ingredient=list(instance.data_dict.keys())[instance.count]
            )
        elif stage in (9, 11, 13, 15):
            message_answer = const.ASK_LIST_OTHER

        if stage in (1, 3, 5):
            buttons = ReplyKeyboardRemove()
            next_state = ChangingData.add
        elif stage in (11, 13, 15):
            buttons = button_generator(
                instance.data_list, ["готово"], without_cancel=True
            )
            next_state = FillingStates.waiting_for_products_list
        else:
            buttons = button_generator(
                instance.data_list, ["готово"], without_cancel=True
            )
            next_state = FillingStates.waiting_for_products_list

    elif user_answer == actions[3]:  # Начать заполнение заново
        instance.current_data_list = []

        if stage in (1, 2, 5, 9, 11, 13, 15):
            message_answer = const.ASK_LIST
        elif stage == 3:
            message_answer = const.ASK_LIST.format(
                ingredient=list(instance.data_dict.keys())[instance.count]
            )

        if stage in (1, 3, 5):
            buttons = ReplyKeyboardRemove()
            next_state = FillingStates.waiting_for_data_list
        elif stage in (2, 9, 11, 13, 15):
            if stage in (9, 11, 13, 15):
                instance.current_data = instance.current_data_list
                if stage == 15:
                    instance.positions_products = sorted(
                        list(set(instance.positions + instance.products))
                    )
                    instance.data_list = instance.positions_products.copy()
                    instance.data_list_copy = instance.data_list.copy()
            instance.data_list = instance.data_list_copy.copy()
            next_state = FillingStates.waiting_for_products_list
            buttons = button_generator(
                instance.data_list, ["готово"], without_cancel=True
            )

    return (message_answer, buttons, next_state)
