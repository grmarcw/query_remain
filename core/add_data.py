from bot.buttons import buttons_yes_or_not
from bot.states_fsm import FillingStates
from core import renderers


def add(data_string, instance):
    data_list = renderers.convert_string_to_list(data_string)

    stage = instance.survey_stage

    if data_string == "отменить":
        message_answer = renderers.render_list_or_dict(
            instance.current_data, stage, instance.positions_products
        )
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation

    else:
        for element in data_list:
            if element not in instance.current_data_list:
                instance.current_data_list.append(element)

        message_answer = renderers.render_list_or_dict(
            instance.current_data, stage, instance.positions_products
        )
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation

    return (message_answer, buttons, next_state)
