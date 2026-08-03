from aiogram.types import ReplyKeyboardRemove

from bot.buttons import button_generator, buttons_show_delete, buttons_yes_or_not
from bot.states_fsm import DeleteStates, FillingStates, States
from constants import constants
from core import renderers
from database import queries


async def handle_show_or_delete_request(user_answer, instance):
    '''
    обрабатывает ответ пользователя для отображения или удаления данных
    :param user_answer: ответ пользователя
    :param instance: экземпляр пользователя
    '''
    if user_answer in ("удалить", "удалить данные"):
        return (
            constants.INPUT_DATA_FOR_DELETE.format(sep=constants.SEPARATOR,data='  •Все данные'),
            button_generator(['Все данные']),
            DeleteStates.waiting_for_deletion_data_type,
        )
    elif user_answer in ("отобразить", "отобразить данные"):
        user_data_from_db = await queries.get_user_data(instance.id_user)
        return (
        f'{renderers.show_recipes(user_data_from_db.recipes)}\n{constants.INPUT_START}',
            ReplyKeyboardRemove(),
            States.clear
        )
    else:
        return (
            constants.SHOW_OR_DELETE,
            buttons_show_delete(),
            None
        )


async def delete_data_from_db(user_answer, instanse):
    if user_answer == 'отменить':
        return (
            f'{constants.OPERATION_CANCEL}\n{constants.INPUT_START}',
            ReplyKeyboardRemove(),
            States.clear
        )
    elif user_answer == 'все данные':
        await queries.delete_user(instanse.id_user)
        return (
            f'{constants.DATA_IS_DELETED}\n{constants.INPUT_START}',
            ReplyKeyboardRemove(),
            States.clear
        )

def delete_element(element, instance):
    s_s = instance.survey_stage
    compositions = instance.compositions
    ingredient_list = instance.ingredients
    cifc = instance.cifc

    if s_s == 1:
        list_for_delete = ingredient_list
    elif s_s == 2:
        list_for_delete = compositions[cifc]

    if element == "отменить":
        next_state = FillingStates.waiting_for_data_confirmation
        if s_s == 1:
            return (
                renderers.render_list(ingredient_list),
                buttons_yes_or_not(),
                next_state
            )
        elif s_s == 2:
             return (
                 renderers.render_dict(compositions, instance.product_is_ingredient),
                 buttons_yes_or_not(),
                 next_state
             )
    elif element in list_for_delete:
        list_for_delete.remove(element)
        next_state = FillingStates.waiting_for_data_confirmation
        if s_s == 1:
            return (
            f'{constants.POSITION_IS_DELETED.format(position=element)}\n{renderers.render_list(ingredient_list)}',
                buttons_yes_or_not(),
                next_state
            )
        elif s_s == 2:
            return (
                f'{constants.PRODUCT_IS_DELETED.format(product=element)}\n{renderers.render_dict(compositions, instance.product_is_ingredient)}',
                buttons_yes_or_not(),
                next_state
            )
    else:
        return (
            constants.PRODUCT_DONT_EXIST.format(list_change='\n'.join(list_for_delete)),
            button_generator(list_for_delete),
            None
            )
