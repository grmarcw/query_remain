from aiogram.types import ReplyKeyboardRemove

from bot.buttons import buttons_yes_or_not, button_generator, buttons_choose_action
from bot.states_fsm import FillingStates, ChangingData
from constants import constants as answer
from core import renderers


def get_element_for_change(element, inst):
    if inst.survey_stage == 1:
        changing_list = inst.ingredients
        inst.cifc = element
    elif inst.survey_stage == 2:
        changing_list = inst.compositions[inst.cifc]
        inst.pfc = element
    else:
        changing_list = []



    if element == "отменить":
        next_state = FillingStates.waiting_for_data_confirmation
        if inst.survey_stage == 1:
            return(
                renderers.render_list(changing_list, inst.data_filling_stage),
                buttons_yes_or_not(),
                next_state
            )
        elif inst.survey_stage == 2:
            return (
                renderers.render_dict(inst.compositions, inst.product_is_ingredient),
                buttons_yes_or_not(),
                next_state
            )
    elif element not in changing_list:
        if inst.data_filling_stage == 1:
            dont_exist = answer.POSITION_DONT_EXIST
        else:
            dont_exist = answer.DELIVERIER_DONT_EXIST
        return (
            dont_exist.format(data_for_changing="\n•".join(changing_list)),
            button_generator(changing_list),
            None
        )
    elif element in changing_list:
        return (
            answer.INPUT_NEW_NAME,
            ReplyKeyboardRemove(),
            ChangingData.change
        )

def change_data(user_answer, instance):

    if instance.survey_stage == 1:
        list_for_change = instance.ingredients
        element_for_change = instance.cifc
    elif instance.survey_stage == 2:
        list_for_change = instance.compositions[instance.cifc]
        element_for_change = instance.pfc

    if user_answer == "отменить":
        next_stage = FillingStates.waiting_for_data_confirmation
        if instance.survey_stage == 1:
            return (
                renderers.render_list(instance.ingredients, instance.data_filling_stage),
                buttons_yes_or_not(),
                next_stage
            )
        elif instance.survey_stage == 2:
            return (
                renderers.render_dict(instance.compositions, instance.product_is_ingredient),
                buttons_yes_or_not(),
                next_stage
            )
    else:
        index = list_for_change.index(element_for_change)
        list_for_change[index] = user_answer
        next_state = FillingStates.waiting_for_data_confirmation
        if instance.survey_stage == 1:
            return (
                renderers.render_list(list_for_change, instance.data_filling_stage),
                buttons_yes_or_not(),
                next_state
            )
        elif instance.survey_stage == 2:
            if user_answer == instance.cifc:
                del instance.compositions[user_answer]
                instance.product_is_ingredient.append(user_answer)
                instance.ingredients_without_products.remove(user_answer)
            return (
                renderers.render_dict(instance.compositions, instance.product_is_ingredient),
                buttons_yes_or_not(),
                next_state)

def get_composition_for_change(user_answer, instance):

    if user_answer == "отменить":
        if instance.survey_stage == 2:
            return (
                renderers.render_dict(instance.compositions, instance.product_is_ingredient),
                buttons_yes_or_not(),
                FillingStates.waiting_for_data_confirmation
                )
        elif instance.survey_stage == 3:
            return (
                    answer.CHECKING_CORRECT_DATA.format(
                        sep=answer.SEPARATOR, checking_data=renderers.show_recipes(instance.recipes)
                    ),
                    buttons_yes_or_not(),
                    FillingStates.waiting_for_data_confirmation
                )
    elif user_answer not in list(instance.compositions.keys()):
        if instance.survey_stage == 2:
            return (
                    answer.POSITION_DONT_EXIST.format(data_for_changing=renderers.render_dict(instance.compositions, option=2)),
                    button_generator(list(instance.compositions.keys())),
                None
                )
        elif instance.survey_stage == 3:
            return (
                    answer.POSITION_DONT_EXIST.format(data_for_changing="\n•".join(list(instance.recipes[instance.pfc].keys()))),
                    button_generator(list(instance.recipes[instance.pfc])),
                    None
                )
    else:
        if instance.survey_stage == 2:
            instance.cifc = user_answer
            return (
                answer.CHOOSE_POSITION_FOR_CHANGE.format(sep=answer.SEPARATOR,choose_list= answer.CHOOSING_ACTION),
                buttons_choose_action(),
                ChangingData.waiting_result_choosing_action
            )
        elif instance.survey_stage == 3:
            instance.cifc = user_answer
            return (
                answer.ASK_QUANTITY.format(ingr=user_answer, product=instance.pfc),
                ReplyKeyboardRemove(),
                ChangingData.waiting_new_quantity
            )

def recomposites(user_answer, instance):
    if str(user_answer).isdigit():
        instance.compositions[instance.cifc] = user_answer
        return (
            renderers.render_dict(instance.compositions, instance.product_is_ingredient),
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation
        )
    else:
        return (
        f'{answer.INCORRECT_INPUT}\n{answer.ASK_QUANTITY.format(ingr=instance.cil[instance.idx_ing], product=instance.cpl[instance.idx_prd])}',
            ReplyKeyboardRemove(),
            None
        )

def get_position_name_for_change(user_answer, instance):

    if user_answer == "отменить":
        return (
            answer.CHECKING_CORRECT_DATA.format(
                sep=answer.SEPARATOR, checking_data=renderers.show_recipes(instance.recipes)
            ),
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation
        )
    elif user_answer in list(instance.recipes.keys()):
        instance.pfc = user_answer
        return (
            answer.ASK_POSITION_FOR_CHANGE,
            button_generator(list(instance.recipes[user_answer].keys())),
            ChangingData.waiting_ingredient_name
        )
    else:
        return (
            answer.PRODUCT_DONT_EXIST.format(list_change="\n•".join(list(instance.recipes.keys()))),
            button_generator(list(instance.recipes.keys())),
            None
        )

def change_quantity(user_answer, instance):
    if str(user_answer).isdigit():
        instance.recipes[instance.pfc][instance.cifc] = user_answer
        return (
            answer.CHECKING_CORRECT_DATA.format(
                sep=answer.SEPARATOR, checking_data=renderers.show_recipes(instance.recipes)
            ),
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation
        )
    else:
        return (
        f'{answer.INCORRECT_INPUT}\n{answer.ASK_QUANTITY.format(ingr=instance.cifc, product=instance.pfc)}',
            ReplyKeyboardRemove(),
            None
        )