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
            try:
                return (
                    constants.ASK_LIST_POSITIONS.format(ingredient=instance.ingredients_without_products[instance.count]),
                    ReplyKeyboardRemove(),
                    None
                )
            except IndexError:
                instance.survey_stage = 2
                return (
                    renderers.render_dict(instance.compositions, list_for_add=instance.product_is_ingredient),
                    buttons_yes_or_not(),
                    FillingStates.waiting_for_data_confirmation
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
        elif instance.data_filling_stage == 3:
            await queries.add_initial_balance(instance.id_user, instance.compositions)
            data = renderers.render_dict_balance(instance.compositions)
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


def get_quantity_balance(quantity, instance):

    if instance.filling_stage == 2:
        incorrect_input = f'''{constants.INCORRECT_INPUT}
{constants.INPUT_SOLD_PRODUCT_QUANTITY.format(product=instance.products[instance.count])}'''

    else:
        incorrect_input = f'''{constants.INCORRECT_INPUT}
{constants.ASK_QUANTITY_BALANCE.format(position=instance.ingredients[instance.count])}'''

    if not str(quantity).isdigit():
        return (
            incorrect_input,
            ReplyKeyboardRemove(),
            None
        )

    if instance.filling_stage == 1:
        instance.compositions.setdefault(instance.ingredients[instance.count], quantity)
        iteration_list = instance.ingredients
    elif instance.filling_stage == 2:
        instance.compositions.setdefault(instance.products[instance.count], quantity)
        iteration_list = instance.products

    instance.count += 1

    if instance.count < len(iteration_list):
        if instance.filling_stage == 2:
            next_message = constants.INPUT_SOLD_PRODUCT_QUANTITY.format(product=instance.products[instance.count])
        else:
            next_message = constants.ASK_QUANTITY_BALANCE.format(position=instance.ingredients[instance.count])
        return (
            next_message,
            ReplyKeyboardRemove(),
            None)
    else:
        instance.survey_stage = 3
        instance.data_filling_stage = 3

        confirm = renderers.render_dict_balance(instance.compositions)
        return (
            confirm,
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation
        )

def get_deliveries(user_answer, instance):
    if instance.filling_stage == 5:
        no_more = constants.NO_MORE_SHIPMENT
        data_list = instance.shipment_in_date
        del_or_pos_list = instance.positions
        other_input = constants.INPUT_OTHER_SHIPMENT
        stage = 4
        filling_stage = 6
    elif instance.filling_stage == 7:
        no_more = constants.NO_MORE_SHIPMENT
        data_list = instance.shipment_out_in_date
        del_or_pos_list = instance.positions
        other_input = constants.INPUT_OTHER_SHIPMENT
        stage = 4
        filling_stage = 7
    else:
        no_more = constants.NO_MORE
        data_list = instance.deliveries_in_date
        del_or_pos_list = list(instance.delivery.keys())
        other_input = constants.INPUT_OTHER_DELIVERIES
        stage = 3
        filling_stage = 3

    if user_answer == no_more:
        instance.survey_stage = 1
        instance.filling_stage = filling_stage
        instance.data_filling_stage = 4
        return (
            renderers.render_list(data_list, stage),
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation
        )
    if user_answer not in del_or_pos_list:
        return (
            f'{constants.DELIVERIER_DONT_EXIST_WITHOUT_FORMAT}',
            button_generator(del_or_pos_list, [no_more], without_cancel=True),
            None
        )
    else:
        if user_answer not in data_list:
            data_list.append(user_answer)

    if user_answer != no_more:
        return (
            other_input,
            button_generator(del_or_pos_list, [no_more], without_cancel=True),
            None
        )

    else:
        instance.survey_stage = 1
        instance.filling_stage = filling_stage
        instance.data_filling_stage = 4
        return (
            renderers.render_list(instance.data_list, stage),
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation
        )

