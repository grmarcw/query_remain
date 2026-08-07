from aiogram.types import ReplyKeyboardRemove

from bot.buttons import button_generator, buttons_show_delete, buttons_yes_or_not
from bot.states_fsm import DeleteStates, FillingStates, States
from constants import constants
from core import renderers
from database import queries
from database.models import SecondaryData


async def handle_show_or_delete_request(user_answer, instance):
    '''
    обрабатывает ответ пользователя для отображения или удаления данных
    :param user_answer: ответ пользователя
    :param instance: экземпляр пользователя
    '''
    if user_answer in ("удалить", "удалить данные"):
        output = '  •Все данные\n  •Данные о поставках\n  •Данные о начальном остатке продукции'
        return (
            constants.INPUT_DATA_FOR_DELETE.format(sep=constants.SEPARATOR,data=output),
            button_generator(['Все данные', 'Данные о поставках', 'Данные об остатке продукции']),
            DeleteStates.waiting_for_deletion_data_type
        )
    elif user_answer in ("отобразить", "отобразить данные"):
        output = []
        user_data_from_db = await queries.get_user_data(instance.id_user)
        data_balance = await queries.get_user_data(instance.id_user, SecondaryData)
        if user_data_from_db is None:
            output.append(f'Данные еще не заполнены\n{constants.INPUT_START}')
        else:
            output.append('Данные о рецептах:\n')
            output.append(renderers.show_recipes(user_data_from_db.recipes))
            output.append(constants.SEPARATOR)

            if user_data_from_db.deliveries is not None:
                output.append('Данные о поставках:\n')
                output.append(renderers.render_dict(user_data_from_db.deliveries, option=3, stage=2))
                output.append(constants.SEPARATOR)

            if data_balance.initial_balance is not None:
                output.append('Данные о начальном остатке продукции:\n')
                output.append(renderers.render_dict_balance(data_balance.initial_balance, option=2))
                output.append(constants.INPUT_START)

        return (
            '\n'.join(output),
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
    elif user_answer in ('все данные', 'данные о поставках', 'данные об остатке продукции'):
        if user_answer == 'все данные':
            await queries.delete_user(instanse.id_user)
            await queries.delete_user(instanse.id_user, SecondaryData)
        elif user_answer == 'данные о поставках':
            await queries.delete_delivery(instanse.id_user)
        elif user_answer == 'данные об остатке продукции':
            await queries.delete_user(instanse.id_user, SecondaryData)
        return (
            f'{constants.DATA_IS_DELETED}\n{constants.INPUT_START}',
            ReplyKeyboardRemove(),
            States.clear
        )
    else:
        return (
            constants.INPUT_DATA_FOR_DELETE.format(sep=constants.SEPARATOR,data='  •Все данные\n  •Данные о поставках'),
            button_generator(['Все данные', 'Данные о поставках']),
            None
        )

def delete_element(element, instance):
    s_s = instance.survey_stage
    compositions = instance.compositions

    if s_s == 1:
        if instance.data_filling_stage != 4:
            list_for_delete = instance.ingredients
        else:
            if instance.filling_stage == 6:
                list_for_delete = instance.shipment_in_date
            elif instance.filling_stage == 7:
                list_for_delete = instance.shipment_out_in_date
            else:
                list_for_delete = instance.deliveries_in_date
    elif s_s == 2:
        list_for_delete = compositions[instance.cifc]

    if element == "отменить":
        next_state = FillingStates.waiting_for_data_confirmation
        if s_s == 1:
            if instance.data_filling_stage != 4:
                output = renderers.render_list(instance.ingredients, instance.data_filling_stage)
            else:
                output = renderers.render_list(list_for_delete, stage=3)
            return (
                output,
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
            if instance.data_filling_stage == 1:
                deleted = constants.POSITION_IS_DELETED
                output = renderers.render_list(instance.ingredients, instance.data_filling_stage)
            else:
                if instance.data_filling_stage == 4:
                    if instance.filling_stage in (6,7):
                        deleted = constants.SHIPMENT_IS_DELETED
                        output = renderers.render_list(list_for_delete, stage=4)
                    else:
                        deleted = constants.DELIVERIER_IS_DELETED
                        output = renderers.render_list(list_for_delete, stage=3)
            return (
            f'{deleted.format(position=element)}\n{output}',
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
        if instance.data_filling_stage == 1:
            dont_exist = constants.PRODUCT_DONT_EXIST
        else:
            if instance.filling_stage in (6,7):
                dont_exist = constants.POSITION_DONT_EXIST
            else:
                dont_exist = constants.DELIVERIER_DONT_EXIST
        return (
            dont_exist.format(data_for_changing='\n'.join(list_for_delete)),
            button_generator(list_for_delete),
            None
            )
