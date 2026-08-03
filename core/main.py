from aiogram.types import ReplyKeyboardRemove

from bot.buttons import buttons_yes_or_not, button_generator
from bot.states_fsm import FillingStates, States
from constants import constants
from core import renderers
from database import queries


def get_composition(product_list, instance):

    if instance.ingredients_without_products == []:
        instance.ingredients_without_products.extend(instance.ingredients)
    product_list = renderers.convert_string_to_list(product_list)
    if instance.ingredients_without_products[instance.count] == product_list[0]:
        instance.product_is_ingredient.append(product_list[0])
        instance.ingredients_without_products.remove(instance.ingredients_without_products[instance.count])
        if len(instance.ingredients_without_products) > 0:
            return (
                constants.ASK_LIST_POSITIONS.format(ingredient=instance.ingredients_without_products[instance.count]),
                ReplyKeyboardRemove(),
                None
            )
        else:
            return (
                constants.CONFIRM_SAVING,
                buttons_yes_or_not(),
                States.waiting_save_confirmation
            )
    else:
        instance.compositions.setdefault(instance.ingredients_without_products[instance.count], product_list)

    instance.count += 1

    if instance.count < len(instance.ingredients_without_products):
        return (
            constants.ASK_LIST_POSITIONS.format(ingredient=instance.ingredients_without_products[instance.count]),
            ReplyKeyboardRemove(),
            None
        )
    else:
        instance.survey_stage = 2
        return (
            renderers.render_dict(instance.compositions, list_for_add=instance.product_is_ingredient),
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation
        )


def get_quantity_ingredients(quantity, instance):

    if str(quantity).isdigit():
        instance.recipes[instance.cpl[instance.idx_prd]][instance.cil[instance.idx_ing]] = quantity
    else:
        return (
        f'{constants.INCORRECT_INPUT}\n{constants.ASK_QUANTITY.format(ingr=instance.cil[instance.idx_ing], product=instance.cpl[instance.idx_prd])}',
            ReplyKeyboardRemove(),
            None
        )

    instance.idx_ing +=1

    if instance.idx_ing < len(instance.cil):
        return (
            constants.ASK_QUANTITY.format(ingr=instance.cil[instance.idx_ing],product=instance.cpl[instance.idx_prd]),
            ReplyKeyboardRemove(),
            None
        )
    else:
        if instance.idx_prd < len(instance.cpl) - 1:
            instance.idx_prd += 1
            instance.idx_ing = 0
            instance.cil = list(instance.recipes[instance.cpl[instance.idx_prd]].keys())
            return (
                constants.ASK_QUANTITY.format(ingr=instance.cil[instance.idx_ing],product=instance.cpl[instance.idx_prd]),
                ReplyKeyboardRemove(),
                None
            )
        else:
            instance.survey_stage = 3
            return (
                constants.CHECKING_CORRECT_DATA.format(
                    sep=constants.SEPARATOR, checking_data=renderers.show_recipes(instance.recipes)
                ),
                buttons_yes_or_not(),
                FillingStates.waiting_for_data_confirmation
            )

async def saving(user_answer, instance):

    if user_answer == "да":
        if instance.data_filling_stage == 1:
            for product in instance.product_is_ingredient:
                instance.recipes.setdefault(product, {})
                instance.recipes[product][product] = 1
            await queries.add_new_user(instance.id_user, instance.recipes)
            data = renderers.show_recipes(instance.recipes)
        elif instance.data_filling_stage == 2:
            await queries.add_deliveries_info(instance.id_user, instance.compositions)
            data = renderers.render_dict(instance.compositions, option=2)
        return (
            f'{constants.SHOW_SAVING_DATA.format(data=data)}\n\n{constants.INPUT_START}',
            ReplyKeyboardRemove(),
            States.clear
        )
    else:
        return (
            constants.CHECKING_CORRECT_DATA.format(
                sep=constants.SEPARATOR, checking_data=renderers.show_recipes(instance.recipes)
            ),
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation
        )


async def get_delivery_composition(deliverier, instance):
    if deliverier not in instance.ingredients:
        return (
            f'{constants.INCORRECT_INPUT}\n{constants.ASK_COMPOSITION_DELIVERY.format(position=instance.full_ingredients_list[instance.count])}',
            button_generator(instance.ingredients, without_cancel=True),
            None
        )

    instance.compositions.setdefault(deliverier, [])
    instance.compositions[deliverier].append(instance.full_ingredients_list[instance.count])

    instance.count += 1

    if instance.count < len(instance.full_ingredients_list):
        return (
            constants.ASK_COMPOSITION_DELIVERY.format(position=instance.full_ingredients_list[instance.count]),
            button_generator(instance.ingredients, without_cancel=True),
            FillingStates.waiting_for_delivery_data_composition
        )
    else:
        instance.survey_stage = 2
        return (
            constants.CHECKING_CORRECT_DATA.format(sep=constants.SEPARATOR, checking_data=renderers.render_dict(instance.compositions, option=2, stage=2)),
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation
        )