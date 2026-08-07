from bot.buttons import buttons_yes_or_not
from bot.states_fsm import FillingStates
from core import transformers, renderers


def add_data_in_instance(user_answer, instance):
    user_answer = renderers.convert_string_to_list(user_answer)
    next_state = FillingStates.waiting_for_data_confirmation
    if instance.survey_stage == 1:
        if instance.data_filling_stage != 4:
            instance.ingredients.extend(user_answer)
            output = renderers.render_list(instance.ingredients, instance.data_filling_stage)
        else:
            output = renderers.render_list(instance.deliveries_in_date, stage=3)
        return (
            output,
            buttons_yes_or_not(),
            next_state
        )
    elif instance.survey_stage == 2:
        instance.compositions[instance.cifc].extend(user_answer)
        return (
            renderers.render_dict(instance.compositions, instance.product_is_ingredient),
            buttons_yes_or_not(),
            next_state
        )