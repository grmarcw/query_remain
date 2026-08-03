from aiogram.types import ReplyKeyboardRemove

from bot.buttons import buttons_choose_action, button_generator, buttons_yes_or_not, buttons_show_delete
from bot.context import RecipesData
from bot.states_fsm import States, ChangingData, DeleteStates, FillingStates
from constants import constants
from core import transformers, renderers
from database import queries


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
            return (
                constants.ASK_SHOW_DELETE,
                buttons_show_delete(),
                DeleteStates.waiting_for_delete_or_display
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
            return (
                constants.ASK_LIST_POSITIONS.format(ingredient=instance.ingredients[0]),
                ReplyKeyboardRemove(),
                FillingStates.waiting_for_data_for_composition
            )
    elif user_answer == "нет" and instance.survey_stage == 1:
        if instance.data_filling_stage == 1:
            choose_list = constants.CHOOSING_ACTION
        else:
            choose_list = constants.CHOOSING_ACTION_DELIVERY
        return (
            constants.CHOOSE_POSITION_FOR_CHANGE.format(sep=constants.SEPARATOR, choose_list=choose_list),
            buttons_choose_action(instance.data_filling_stage),
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
        return (
            constants.CONFIRM_SAVING,
            buttons_yes_or_not(),
            States.waiting_save_confirmation
        )
    elif user_answer == 'нет' and instance.survey_stage == 3:
        recipes = instance.recipes
        positions_list = list(recipes.keys())
        instance.cpl = positions_list

        return (
            constants.ASK_PRODUCT_FOR_CHANGE,
            button_generator(positions_list),
            ChangingData.waiting_position_name_for_change
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
        item = 'поставщика'

    s_s = instance.survey_stage
    actions = [f"поменять {item}", f"удалить {item}", f"добавить {item}", "начать заполнение заново", "отменить"]

    if instance.data_filling_stage == 1:
        change = constants.ASK_POSITION_FOR_CHANGE
        delete = constants.ASK_POSITION_FOR_DELETE
        add = constants.ASK_LIST_INGREDIENTS
    else:
        change = constants.ASK_DELIVERIER_FOR_CHANGE
        delete =constants.ASK_DELIVERIER_FOR_DELETE
        add = constants.ASK_DELIVERIES_LIST

    if user_answer == actions[0] and s_s == 1:
        return (
            change,
            button_generator(instance.ingredients),
            ChangingData.waiting_element_for_change
        )
    elif user_answer == actions[1] and s_s == 1:
        return (
            delete,
            button_generator(instance.ingredients),
            ChangingData.delete
        )
    elif user_answer == actions[2] and s_s == 1:
        return (
            add,
            ReplyKeyboardRemove(),
            ChangingData.add
        )
    elif user_answer == actions[3] and s_s == 1:
        return (
            add,
            ReplyKeyboardRemove(),
            FillingStates.waiting_for_data_list
        )
    elif user_answer == actions[4] and s_s == 1:
        return (
            renderers.render_list(instance.ingredients, instance.data_filling_stage),
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
            f'{constants.INCORRECT_INPUT}\n{constants.CHOOSING_ACTION}',
            buttons_choose_action(),
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