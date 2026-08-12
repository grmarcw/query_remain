from aiogram.types import ReplyKeyboardRemove
from black import const
from pygments.lexer import include

from bot.buttons import buttons_yes_or_not, button_generator
from bot.states_fsm import FillingStates, States
from constants import general, stage_2
from core import renderers, import_loader
from database import queries
from database.models import SecondaryData


def get_data_list(data_string, instance):
    stage = instance.survey_stage
    data_list = renderers.convert_string_to_list(data_string)
    data_list_without_copy = []
    for element in data_list:
        if element not in data_list_without_copy:
            data_list_without_copy.append(element)

    if instance.survey_stage != 3:
        instance.current_data_list = data_list_without_copy
        instance.current_data = instance.current_data_list
    else:
        instance.data_dict[list(instance.data_dict.keys())[instance.count]] = (
            data_list_without_copy
        )

    message_answer = renderers.render_list_or_dict(
        instance.current_data, stage, instance.positions_products
    )
    buttons = buttons_yes_or_not()
    next_state = FillingStates.waiting_for_data_confirmation

    return (message_answer, buttons, next_state)


def get_products(product, instance):

    stage = instance.survey_stage
    const = import_loader.get_constants(stage)

    if product == "готово":
        message_answer = renderers.render_list_or_dict(
            instance.current_data_list, stage, instance.positions_products
        )
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation
    elif product in instance.data_list:
        instance.data_list.remove(product)
        instance.current_data_list.append(product)

        message_answer = const.ASK_LIST
        buttons = button_generator(instance.data_list, ["готово"], without_cancel=True)
        next_state = None
    elif product in instance.current_data_list:
        message_answer = const.ALREADY_EXIST + const.ASK_LIST
        buttons = button_generator(instance.data_list, ["готово"], without_cancel=True)
        next_state = None
    else:
        message_answer = const.DONT_EXIST + const.ASK_LIST
        buttons = button_generator(instance.data_list, ["готово"], without_cancel=True)
        next_state = None

    return (message_answer, buttons, next_state)


def get_composition(product_string, instance):
    # count - счетчик позиций(ингредиентов)
    stage = instance.survey_stage
    const = import_loader.get_constants(stage)

    product_list = renderers.convert_string_to_list(product_string)
    positions = instance.data_list

    instance.data_dict.setdefault(positions[instance.count], [])
    instance.data_dict[positions[instance.count]].extend(product_list)
    instance.count += 1

    if instance.count < len(instance.data_list):
        message_answer = const.ASK_LIST.format(
            position=instance.data_list[instance.count]
        )
        buttons = ReplyKeyboardRemove()
        next_state = None
    else:
        instance.count = 0

        message_answer = renderers.render_list_or_dict(
            instance.current_data, stage, instance.positions_products
        )
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation

    return (message_answer, buttons, next_state)


def get_quantity(quantity, instance):

    stage = instance.survey_stage

    const = import_loader.get_constants(stage)

    try:
        float(quantity)
    except ValueError:
        if stage == 4:
            output = general.INCORRECT_INPUT + const.ASK_QUANTITY.format(
                position=instance.current_position_for_change,
                product=instance.current_data_list[instance.count],
            )
        elif stage == 10:
            output = general.INCORRECT_INPUT + const.ASK_QUANTITY.format(
                position=instance.current_data_list[instance.count]
            )
        return (output, ReplyKeyboardRemove(), None)
    if stage == 4:
        product = instance.current_data_list[instance.count]
        position = instance.current_position_for_change
    elif stage == 12 or stage == 10:
        product = instance.current_position_for_change
        position = instance.current_data_list[instance.count]

    instance.recipes.setdefault(product, {})
    instance.recipes[product][position] = quantity

    instance.count += 1

    if instance.count < len(instance.current_data_list):
        if stage == 4:
            output = const.ASK_QUANTITY.format(
                position=instance.current_position_for_change,
                product=instance.current_data_list[instance.count],
            )
        elif stage == 10:
            output = const.ASK_QUANTITY.format(
                position=instance.current_data_list[instance.count]
            )
        message_answer = output
        buttons = ReplyKeyboardRemove()
        next_state = None
    else:
        instance.count_two += 1
        instance.count = 0
        if instance.count_two < len(instance.data_list):
            instance.current_position_for_change = instance.data_list[
                instance.count_two
            ]
            instance.current_data_list = instance.data_dict[
                instance.current_position_for_change
            ]

            if stage == 4:
                output = const.ASK_QUANTITY.format(
                    position=instance.current_position_for_change,
                    product=instance.current_data_list[instance.count],
                )
            elif stage == 10:
                output = const.ASK_QUANTITY.format(
                    position=instance.current_data_list[instance.count]
                )
            message_answer = output
            buttons = ReplyKeyboardRemove()
            next_state = None
        else:
            instance.count = 0
            instance.count_two = 0

            message_answer = renderers.render_list_or_dict(instance.current_data, stage)
            buttons = buttons_yes_or_not()
            next_state = FillingStates.waiting_for_data_confirmation

    return (message_answer, buttons, next_state)


async def saving(user_answer, instance):
    stage = instance.survey_stage

    if user_answer == "да":
        if stage == 4:
            await queries.add_new_user(instance.user_id, instance.recipes)
            await queries.add_new_info(
                instance.user_id, "positions_products", instance.positions_products
            )
        elif stage == 6:
            await queries.add_new_info(
                instance.user_id, "deliveries", instance.data_dict
            )
        elif stage == 7:
            await queries.add_initial_balance(instance.user_id, instance.data_dict)

        elif stage == 17:
            dict_for_saving = {}
            dict_for_saving[instance.date] = instance.dict_in_dict
            instance.current_data = dict_for_saving

            await queries.add_daily_data(instance.user_id, dict_for_saving)

        message_answer = general.SHOW_SAVING_DATA.format(
            data=renderers.render_list_or_dict(
                instance.current_data, stage, instance.positions_products, 2
            )
        )
        buttons = ReplyKeyboardRemove()
        next_state = States.clear
    else:
        message_answer = (
            renderers.render_list_or_dict(
                instance.current_data, stage, instance.positions_products
            )
        )
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation

    return (message_answer, buttons, next_state)


async def get_delivery_composition(deliverer, instance):
    stage = instance.survey_stage
    const = import_loader.get_constants(stage)

    if deliverer not in list(instance.data_dict.keys()):
        return (
            f"{general.INCORRECT_INPUT}\n{const.ASK_LIST.format(position=instance.current_position_for_change)}",
            button_generator(list(instance.data_dict.keys()), without_cancel=True),
            None,
        )

    instance.data_dict[deliverer].append(instance.current_position_for_change)

    instance.count += 1

    if instance.count < len(instance.data_list):
        instance.current_position_for_change = instance.data_list[instance.count]
        return (
            const.ASK_LIST.format(position=instance.current_position_for_change),
            button_generator(list(instance.data_dict.keys()), without_cancel=True),
            None,
        )
    else:
        deliveries_for_delete = []
        for deliverer, positions in instance.data_dict.items():
            if positions == []:
                deliveries_for_delete.append(deliverer)
        for deliverer in deliveries_for_delete:
            del instance.data_dict[deliverer]
        return (
            renderers.render_list_or_dict(instance.current_data, stage),
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation,
        )


def get_quantity_balance(quantity, instance):
    stage = instance.survey_stage
    const = import_loader.get_constants(stage)

    try:
        float(quantity)
    except ValueError:
        return (f"{general.INCORRECT_INPUT}\n{const.ASK_QUANTITY.format(
                        position = instance.data_list[instance.count]
                    )}", ReplyKeyboardRemove(), None)

    instance.data_dict.setdefault(instance.data_list[instance.count], quantity)
    instance.count += 1

    if instance.count < len(instance.data_list):
        message_answer = const.ASK_QUANTITY.format(
            position=instance.data_list[instance.count]
        )
        buttons = ReplyKeyboardRemove()
        next_state = None
    else:
        instance.count = 0
        instance.current_data = instance.data_dict
        message_answer = renderers.render_list_or_dict(instance.current_data, stage)
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation

    return (message_answer, buttons, next_state)
