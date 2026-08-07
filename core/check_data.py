from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.util import await_only

from bot.buttons import buttons_choose_action, button_generator, buttons_yes_or_not, buttons_show_delete
from bot.states_fsm import States, ChangingData, DeleteStates, FillingStates, CurrentActualBalance, Main
from constants import constants
from core import transformers, renderers
from database import queries
from database.models import SecondaryData


def init_user_data(instance):
    instance.ingredients = []   # список отслеживаемых ингредиентов
    instance.ingredients_without_products = []
    instance.compositions = {}  # словарь {отслеживаемый ингредиент: [список, из, товаров]}
    instance.recipes = {}       # словарь {товар:{ингредиент: количество}}
    instance.survey_stage = 1            # текущий этап заполнения данных
    instance.product_is_ingredient = []  # список ингредиентов, которые являются товарами
    instance.count = 0                   # универсальный счетчик
    instance.idx_ing = 0                 # индекс ингридиента
    instance.idx_prd = 0                 # индекс продукта
    instance.cpl = []                    # текущий список продуктов
    instance.cil = []                    # текущий список ингридиентов
    instance.cifc = ''                   # текущий ингридиент для изменения
    instance.pfc = ''


async def check_data_in_db(instance):
    data = await queries.get_user_data(instance.id_user)
    if data is None:
        return (
            constants.ASK_LIST_INGREDIENTS,
            ReplyKeyboardRemove(),
            FillingStates.waiting_for_data_list
        )
    elif data is not None:
        if data.deliveries is None:
            instance.data_filling_stage = 2
            for recipe in data.recipes.values():
                for ingredient in recipe.keys():
                    if ingredient not in instance.full_ingredients_list:
                        instance.full_ingredients_list.append(ingredient)
            return(
                constants.ASK_DELIVERIES_LIST,
                ReplyKeyboardRemove(),
                FillingStates.waiting_for_data_list
            )
        else:
            if await queries.get_user_data(instance.id_user, SecondaryData):
                return (
                    f'Все первичные данные заполнены',
                    button_generator(['/help'],without_cancel=True),
                    States.clear
                )
            else:
                instance.count = 0
                for recipe in data.recipes.values():
                    for ingredient in recipe.keys():
                        if ingredient not in instance.ingredients:
                            instance.ingredients.append(ingredient)
                return (
                    constants.ASK_QUANTITY_BALANCE.format(position=instance.ingredients[instance.count]),
                    ReplyKeyboardRemove(),
                    CurrentActualBalance.waiting_for_quantity
                )


def give_response_text_for_check_correctness_data(user_answer: str, instance):
    '''
    В зависимости от текущего этапа заполнения данных
    выводит нужный текст для вопроса пользователю
    для проверки корректности данных
    :param survey_stage: текущий этап
    :return: (
    строка для вопроса пользователю,
    настройки для кнопок,
    следующее состояние для FSMContext
    )
    '''
    if user_answer == "да" and instance.survey_stage == 1:
        if instance.data_filling_stage == 2:
            instance.count = 0
            return (
                constants.ASK_COMPOSITION_DELIVERY.format(position=instance.full_ingredients_list[instance.count]),
                button_generator(instance.ingredients, without_cancel=True),
                FillingStates.waiting_for_delivery_data_composition
            )
        else:
            if instance.filling_stage == 3:
                next_question = constants.SHIPMENT_CONFIRM
                button = button_generator(instance.positions, [constants.NO_MORE_SHIPMENT], without_cancel=True)
                next_state = Main.waiting_for_deliveries_names
                instance.filling_stage = 5
            elif instance.filling_stage == 6:
                instance.filling_stage = 7
                next_question = constants.SHIPMENT_CONFIRM_OUT
                button = button_generator(instance.positions, [constants.NO_MORE_SHIPMENT], without_cancel=True)
                next_state = Main.waiting_for_deliveries_names
            elif instance.filling_stage == 7:
                instance.filling_stage = 8
                next_question = None
                button = None
                next_state = None
            else:
                next_question = constants.ASK_LIST_POSITIONS.format(ingredient=instance.ingredients[0])
                button = ReplyKeyboardRemove()
                next_state = FillingStates.waiting_for_data_for_composition
            return (
                next_question,
                button,
                next_state
            )
    elif user_answer == "нет" and instance.survey_stage == 1:
        if instance.data_filling_stage == 1:
            choose_list = constants.CHOOSING_ACTION
        elif instance.data_filling_stage == 4:
            if instance.filling_stage == 3:
                choose_list = constants.CHOOSING_ACTION_DELIVERY_ADD_DELETE
            elif instance.filling_stage in (6,7):
                choose_list = constants.CHOOSING_ACTION_SHIPMENT_ADD_DELETE
        else:
            choose_list = constants.CHOOSING_ACTION_DELIVERY

        if instance.filling_stage in (6,7):
            button = buttons_choose_action(5)
        else:
            button = buttons_choose_action(instance.data_filling_stage)
        return (
            constants.CHOOSE_POSITION_FOR_CHANGE.format(sep=constants.SEPARATOR, choose_list=choose_list),
            button,
            ChangingData.waiting_result_choosing_action
            )


    elif user_answer == "да" and instance.survey_stage == 2:
        if instance.data_filling_stage == 2:
            return (
                constants.CONFIRM_SAVING,
                buttons_yes_or_not(),
                States.waiting_save_confirmation
            )

        recipes = transformers.nest_dict(instance.compositions) #{'позиция':['товар', 'второй товар']} -> {'товар':{'позиция': 0}...}
        instance.recipes = recipes

        first_product = list(recipes.keys())[0]
        first_ingredient = list(recipes[first_product].keys())[0]
        instance.cpl = list(instance.recipes.keys())
        instance.idx_prd = 0
        instance.cil = list(instance.recipes[instance.cpl[0]].keys())
        instance.idx_ing = 0
        instance.count = 0

        return (
            constants.ASK_QUANTITY.format(ingr=first_ingredient, product=first_product),
            ReplyKeyboardRemove(),
            FillingStates.waiting_quantity
        )
    elif user_answer == "нет" and instance.survey_stage == 2:
        if instance.data_filling_stage == 1:
            return (
                constants.ASK_POSITION_FOR_CHANGE,
                button_generator(instance.ingredients_without_products),
                ChangingData.waiting_ingredient_name
            )
        else:
            return (
                constants.ASK_FILLING_DATA_AGAIN,
                buttons_yes_or_not(),
                FillingStates.waiting_for_filling_data_confirmation
            )


    elif user_answer == "да" and instance.survey_stage == 3:
        if instance.filling_stage == 1:
            output = constants.CONFIRM_SAVING
            buttons = buttons_yes_or_not()
            next_state = States.waiting_save_confirmation
        elif instance.filling_stage == 2:
            deliveries_list = list(instance.delivery.keys())
            output = constants.INPUT_DELIVERIES_NAMES
            buttons = button_generator(deliveries_list, [constants.NO_MORE],without_cancel=True)
            next_state = Main.waiting_for_deliveries_names
        return (
            output,
            buttons,
            next_state
        )
    elif user_answer == 'нет' and instance.survey_stage == 3:
        if instance.data_filling_stage < 3:
            recipes = instance.recipes
            positions_list = list(recipes.keys())
            instance.cpl = positions_list
            question = constants.ASK_PRODUCT_FOR_CHANGE
            next_state = ChangingData.waiting_position_name_for_change
        else:
            instance.survey_stage = 1
            question = constants.ASK_POSITION_FOR_CHANGE
            next_state = ChangingData.waiting_element_for_change
            if instance.filling_stage == 1:
                positions_list = instance.ingredients
            elif instance.filling_stage == 2:
                positions_list = instance.products

        return (
            question,
            button_generator(positions_list),
            next_state
        )


    else:
        return (
            constants.INPUT_YES_NO,
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation
        )

def choose_action(user_answer, instance):
    if instance.data_filling_stage == 1:
        item = 'позицию'
    else:
        if instance.filling_stage in (6,7):
            item = 'перемещение'
        else:
            item = 'поставщика'

    s_s = instance.survey_stage
    actions = [f"поменять {item}", f"удалить {item}", f"добавить {item}", "начать заполнение заново", "отменить"]


    if instance.data_filling_stage == 1:
        change = constants.ASK_POSITION_FOR_CHANGE
        delete = constants.ASK_POSITION_FOR_DELETE
        add = constants.ASK_LIST_INGREDIENTS
        choosing_action = constants.CHOOSING_ACTION
        buttons = buttons_choose_action()
    elif instance.data_filling_stage == 4:
        if instance.filling_stage not in (6,7):
            delete = constants.ASK_DELIVERIER_FOR_DELETE
            add = constants.INPUT_DELIVERIES_NAMES
            choosing_action = constants.CHOOSING_ACTION_DELIVERY_ADD_DELETE
            buttons = buttons_choose_action(4)
        else:
            delete = constants.ASK_SHIPMENT_FOR_DELETE
            choosing_action = constants.CHOOSING_ACTION_SHIPMENT_ADD_DELETE
            buttons = buttons_choose_action(5)
            if instance.filling_stage == 6:
                add = constants.SHIPMENT_CONFIRM
            elif instance.filling_stage == 7:
                add = constants.SHIPMENT_CONFIRM_OUT
    else:
        change = constants.ASK_DELIVERIER_FOR_CHANGE
        delete =constants.ASK_DELIVERIER_FOR_DELETE
        add = constants.ASK_DELIVERIES_LIST


    if user_answer == actions[0] and s_s == 1:
        if instance.data_filling_stage != 4:
            return (
                change,
                button_generator(instance.ingredients),
                ChangingData.waiting_element_for_change
            )
        else:
            return (
                f'{constants.INCORRECT_INPUT}\n{choosing_action}',
                buttons_choose_action(4),
                None
            )
    elif user_answer == actions[1] and s_s == 1:
        if instance.data_filling_stage != 4:
            button = button_generator(instance.ingredients)
        else:
            if instance.filling_stage == 6:
                button = button_generator(instance.shipment_in_date)
            elif instance.filling_stage == 7:
                button = button_generator(instance.shipment_out_in_date)
            else:
                button = button_generator(instance.deliveries_in_date)
        return (
            delete,
            button,
            ChangingData.delete
        )
    elif user_answer == actions[2] and s_s == 1:
        if instance.data_filling_stage != 4:
            return (
                add,
                ReplyKeyboardRemove(),
                ChangingData.add
            )
        else:
            if instance.filling_stage == 6:
                instance.filling_stage = 5
                button = button_generator(instance.positions, [constants.NO_MORE_SHIPMENT], without_cancel=True)
            elif instance.filling_stage == 7:
                button = button_generator(instance.positions, [constants.NO_MORE_SHIPMENT], without_cancel=True)
            else:
                button = button_generator(list(instance.delivery.keys()), [constants.NO_MORE], without_cancel=True)
            return (
            add,
            button,
            Main.waiting_for_deliveries_names
         )
    elif user_answer == actions[3] and s_s == 1:
        if instance.data_filling_stage != 4:
            next_state = FillingStates.waiting_for_data_list
            button = ReplyKeyboardRemove()
        else:
            if instance.filling_stage == 6:
                instance.filling_stage = 5
                instance.shipment_in_date = []
                next_state = Main.waiting_for_deliveries_names
                button = button_generator(instance.positions, [constants.NO_MORE], without_cancel=True)
            elif instance.filling_stage == 7:
                instance.shipment_out_in_date = []
                next_state = Main.waiting_for_deliveries_names
                button = button_generator(instance.positions, [constants.NO_MORE], without_cancel=True)
            else:
                instance.deliveries_in_date = []
                next_state = Main.waiting_for_deliveries_names
                button = button_generator(list(instance.delivery.keys()), [constants.NO_MORE], without_cancel=True)
        return (
            add,
            button,
            next_state
        )
    elif user_answer == actions[4] and s_s == 1:
        if instance.data_filling_stage != 4:
            output = renderers.render_list(instance.ingredients, instance.data_filling_stage)
        else:
            if instance.filling_stage == 6:
                output = renderers.render_list(instance.shipment_in_date, 4)
            elif instance.filling_stage == 7:
                output = renderers.render_list(instance.shipment_out_in_date, 4)
            else:
                output = renderers.render_list(instance.deliveries_in_date, stage=3)
        return (
            output,
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation
        )
    elif user_answer == actions[0] and s_s == 2:
        return (
            constants.ASK_PRODUCT_FOR_CHANGE,
            button_generator(instance.compositions[instance.cifc]),
            ChangingData.waiting_element_for_change
        )
    elif user_answer == actions[1] and s_s == 2:
        return (
            constants.ASK_PRODUCT_FOR_DELETE,
            button_generator(instance.compositions[instance.cifc]),
            ChangingData.delete
        )
    elif user_answer == actions[2] and s_s == 2:
        return (
            constants.ASK_LIST_POSITIONS_WITHOUT_PRD_IS_ING.format(
                ingredient=instance.cifc
            ),
            ReplyKeyboardRemove(),
            ChangingData.add
        )
    elif user_answer == actions[3] and s_s == 2:
        instance.compositions[instance.cifc] = []
        return (
            constants.ASK_LIST_POSITIONS.format(ingredient=instance.cifc),
            ReplyKeyboardRemove(),
            ChangingData.add
        )
    elif user_answer == actions[4] and s_s == 2:
        return (
            renderers.render_dict(instance.compositions, instance.product_is_ingredient),
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation
        )
    else:
        return (
            f'{constants.INCORRECT_INPUT}\n{choosing_action}',
            buttons,
            None
        )

def get_confirm(user_answer, instance):
    if user_answer == 'нет':
        return (
            constants.CHECKING_CORRECT_DATA.format(sep=constants.SEPARATOR,
                                                   checking_data=renderers.render_dict(instance.compositions)),
            buttons_yes_or_not(),
            FillingStates.waiting_for_data_confirmation
        )
    elif user_answer == 'да':
        instance.count = 0
        return (
            constants.ASK_COMPOSITION_DELIVERY.format(position=instance.full_ingredients_list[instance.count]),
            button_generator(instance.ingredients, without_cancel=True),
            FillingStates.waiting_for_delivery_data_composition
        )
    else:
        return (
            constants.INPUT_YES_NO,
            buttons_yes_or_not(),
            None
        )