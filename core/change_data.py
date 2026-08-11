from aiogram.types import ReplyKeyboardRemove

from bot.buttons import buttons_yes_or_not, button_generator, buttons_choose_action
from bot.states_fsm import FillingStates, ChangingData
from constants import general as answer, general
from core import renderers, import_loader


def get_element_for_change(element, instance):

    stage = instance.survey_stage
    const = import_loader.get_constants(stage)

    if element == "отменить":
        message_answer = renderers.render_list_or_dict(
            instance.current_data, stage, instance.positions_products
        )
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation

    elif element in instance.current_data_list:
        instance.current_position_for_change = element

        message_answer = const.ASK_NEW_NAME
        next_state = ChangingData.change
        if stage in (1, 3, 5, 7, 8, 10, 12, 14):
            buttons = ReplyKeyboardRemove()
        else:
            buttons = button_generator(instance.data_list)

    else:
        if stage in (9, 11, 12, 15):
            buttons = button_generator(instance.current_data_list)
        else:
            buttons = button_generator(instance.data_list)
        message_answer = const.DONT_EXIST + const.ASK_NAME_FOR_CHANGE
        next_state = None

    return (message_answer, buttons, next_state)


def change(new_name, instance):

    stage = instance.survey_stage

    cpfc = instance.current_position_for_change
    changing_list = instance.current_data_list

    const = import_loader.get_constants(stage)

    if new_name == "отменить":
        message_answer = renderers.render_list_or_dict(
            instance.current_data, stage, instance.positions_products
        )
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation
    elif stage == 4:
        position = instance.current_position_for_change
        product = list(instance.recipes.keys())[instance.count]
        try:
            float(new_name)
        except ValueError:
            return (
                general.INCORRECT_INPUT
                + const.ASK_QUANTITY.format(position=position, product=product),
                ReplyKeyboardRemove(),
                None,
            )
        else:
            instance.current_data[product][position] = new_name
            return (
                renderers.render_list_or_dict(
                    instance.current_data, stage, instance.positions_products
                ),
                buttons_yes_or_not(),
                FillingStates.waiting_for_data_confirmation,
            )

    elif new_name in instance.current_data_list:
        message_answer = const.ALREADY_EXIST + renderers.render_list_or_dict(
            instance.current_data, stage, instance.positions_products
        )
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation
    else:
        if stage in (1, 2, 3, 5, 6, 9, 11, 13, 15):
            if stage in (9, 11, 13):
                if new_name not in instance.data_list:
                    return (
                        general.INCORRECT_INPUT + const.ASK_NEW_NAME,
                        button_generator(instance.data_list),
                        None,
                    )
            index_changing_element = changing_list.index(cpfc)
            instance.current_data_list[index_changing_element] = new_name
        if stage in (2, 9, 11, 13, 15):
            instance.data_list.append(cpfc)
            instance.data_list.remove(new_name)
        elif stage == 3:
            position = list(instance.data_dict.keys())[instance.count]
            instance.data_dict[position] = instance.current_data_list.copy()
            instance.current_position_for_change = None
            instance.current_data_list = []
        elif stage in (7, 8, 12, 14):
            try:
                float(new_name)
                instance.data_dict[instance.current_position_for_change] = new_name
            except ValueError:
                return (
                    general.INCORRECT_INPUT
                    + const.ASK_QUANTITY.format(
                        position=instance.current_position_for_change
                    ),
                    ReplyKeyboardRemove(),
                    None,
                )
        elif stage == 10:
            try:
                float(new_name)
                current_delivery = list(instance.data_dict.keys())[instance.count]
                instance.current_data[current_delivery][
                    instance.current_position_for_change
                ] = new_name
            except ValueError:
                return (
                    general.INCORRECT_INPUT + const.ASK_NEW_NAME,
                    ReplyKeyboardRemove(),
                    None,
                )
        message_answer = renderers.render_list_or_dict(
            instance.current_data, stage, instance.positions_products
        )
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation

    return (message_answer, buttons, next_state)


def get_composition_for_change(position_name, instance):

    stage = instance.survey_stage
    const = import_loader.get_constants(stage)

    if position_name == "отменить":
        message_answer = renderers.render_list_or_dict(
            instance.current_data, stage, instance.positions_products
        )
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation

    elif position_name in list(instance.current_data.keys()):
        instance.count = list(instance.current_data.keys()).index(position_name)
        if stage == 4 or stage == 10:
            instance.current_data_list = list(
                instance.current_data[position_name].keys()
            )
        else:
            instance.current_data_list = instance.current_data[position_name]

        message_answer = const.ASK_CHOOSING_ACTION + const.CHOOSING_ACTION
        buttons = button_generator(const.CHOOSING_ACTION_LIST)
        next_state = ChangingData.waiting_result_choosing_action

    else:
        if stage == 4:
            buttons = button_generator(list(instance.recipes.keys()))
        else:
            buttons = button_generator(instance.data_list)
        message_answer = const.DONT_EXIST + const.ASK_KEY_FOR_CHANGE
        next_state = None

    return (message_answer, buttons, next_state)
