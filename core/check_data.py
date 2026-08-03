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

    if await queries.get_user_data(instance.id_user) is None:
        return (
            constants.ASK_LIST_INGREDIENTS,
            ReplyKeyboardRemove(),
            FillingStates.waiting_for_data_list
        )
    elif await queries.get_user_data(instance.id_user) is not None:
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
        return (
            constants.ASK_LIST_POSITIONS.format(ingredient=instance.ingredients[0]),
            ReplyKeyboardRemove(),
            FillingStates.waiting_for_data_for_composition
        )
    elif user_answer == "нет" and instance.survey_stage == 1:
        return (
            constants.CHOOSE_POSITION_FOR_CHANGE.format(sep=constants.SEPARATOR, choose_list=constants.CHOOSING_ACTION),
            buttons_choose_action(),
            ChangingData.waiting_result_choosing_action
        )


    elif user_answer == "да" and instance.survey_stage == 2:
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
        return (
            constants.ASK_POSITION_FOR_CHANGE,
            button_generator(instance.ingredients_without_products),
            ChangingData.waiting_ingredient_name
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

    s_s = instance.survey_stage

    actions = ("поменять позицию", "удалить позицию", "добавить позицию", "начать заполнение заново", "отменить")

    if user_answer == actions[0] and s_s == 1:
        return (
            constants.ASK_POSITION_FOR_CHANGE,
            button_generator(instance.ingredients),
            ChangingData.waiting_element_for_change
        )
    elif user_answer == actions[1] and s_s == 1:
        return (
            constants.ASK_POSITION_FOR_DELETE,
            button_generator(instance.ingredients),
            ChangingData.delete
        )
    elif user_answer == actions[2] and s_s == 1:
        return (
            constants.ASK_LIST_INGREDIENTS,
            ReplyKeyboardRemove(),
            ChangingData.add
        )
    elif user_answer == actions[3] and s_s == 1:
        return (
            constants.ASK_LIST_INGREDIENTS,
            ReplyKeyboardRemove(),
            FillingStates.waiting_for_data_list
        )
    elif user_answer == actions[4] and s_s == 1:
        return (
            renderers.render_list(instance.ingredients),
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