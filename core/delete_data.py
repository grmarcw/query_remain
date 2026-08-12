from aiogram.types import ReplyKeyboardRemove

from bot.buttons import button_generator, buttons_show_delete, buttons_yes_or_not
from bot.states_fsm import DeleteStates, FillingStates, States, Main, ChangingData
from constants import general
from core import renderers, import_loader
from database import queries
from database.models import SecondaryData


async def handle_show_or_delete_request(user_answer, instance):
    """
    обрабатывает ответ пользователя для отображения или удаления данных
    :param user_answer: ответ пользователя
    :param instance: экземпляр пользователя
    """
    if user_answer in ("удалить", "удалить данные"):
        delete_list = ["Все данные", "Данные о поставках", "Данные об остатке продукции", "Данные за определенную дату"]
        output = '\n  •'.join(delete_list)
        return (
            general.INPUT_DATA_FOR_DELETE.format(sep=general.SEPARATOR, data=output),
            button_generator(
                delete_list
            ),
            DeleteStates.waiting_for_deletion_data_type
        )
    elif user_answer in ("отобразить", "отобразить данные"):
        output = []
        user_data_from_db = await queries.get_user_data(instance.user_id)
        data_balance = await queries.get_user_data(instance.user_id, SecondaryData)

        if user_data_from_db is None:
            output.append(f"Данные еще не заполнены\n{general.INPUT_START}")
        else:
            output.append("Данные о рецептах:\n")
            output.append(
                renderers.render_list_or_dict(user_data_from_db.recipes, 4, option=2)
            )
            if user_data_from_db.positions_products:
                output.append(
                    renderers.render_list_or_dict(
                        user_data_from_db.positions_products, 1, option=67
                    )
                )
                output.append(general.SEPARATOR)
            else:
                output.append(general.SEPARATOR)
            if user_data_from_db.deliveries is not None:
                output.append("Данные о поставках:\n")
                output.append(
                    renderers.render_list_or_dict(
                        user_data_from_db.deliveries, stage=3, option=2
                    )
                )
                output.append(general.SEPARATOR)

            if data_balance is not None:
                output.append("Данные о начальном остатке продукции:\n")
                output.append(
                    renderers.render_list_or_dict(
                        data_balance.initial_balance, 7, option=2
                    )
                )
                if data_balance.data:
                    output.append("Данные по датам\n")
                    output.append(
                        renderers.render_list_or_dict(data_balance.data, 18, option=2)
                    )

        return ("\n".join(output), ReplyKeyboardRemove(), States.clear)
    else:
        return (general.SHOW_OR_DELETE, buttons_show_delete(), None)


async def delete_data_from_db(user_answer, instance):
    user_answer = user_answer.capitalize()
    delete_list = ["Все данные", "Данные о поставках", "Данные об остатке продукции", "Данные за определенную дату"]
    if user_answer == "Отменить":
        return (
            f"{general.OPERATION_CANCEL}\n{general.INPUT_START}",
            ReplyKeyboardRemove(),
            States.clear,
        )
    elif user_answer in delete_list:
        if user_answer == delete_list[0]: #все данные
            await queries.delete_user(instance.user_id)
            await queries.delete_user(instance.user_id, SecondaryData)
        elif user_answer == delete_list[1]: #данные о поставках
            await queries.delete_delivery(instance.user_id)
        elif user_answer == delete_list[2]: #данные об остатке продукции
            await queries.delete_user(instance.user_id, SecondaryData)
        elif user_answer == delete_list[3]: #данные за определенную дату
            data = await queries.get_user_data(instance.user_id, SecondaryData)
            dates = []
            for user_data in data.data:
                for name_column, date in user_data.items():
                    dates.append(name_column)
            instance.data_list = dates
            return (
                "За какую дату вы хотите удалить данные?",
                button_generator(dates),
                ChangingData.waiting_for_date_for_delete
            )
        return (
            f"{general.DATA_IS_DELETED}\n{general.INPUT_START}",
            ReplyKeyboardRemove(),
            States.clear,
        )
    else:
        return (
            general.INPUT_DATA_FOR_DELETE.format(
                sep=general.SEPARATOR, data='\n  •'.join(delete_list)
            ),
            button_generator(delete_list),
            None,
        )

async def delete_date(date, instance):
    delete_list = ["Все данные", "Данные о поставках", "Данные об остатке продукции", "Данные за определенную дату"]
    if date == 'отменить':
        return (
            general.INPUT_DATA_FOR_DELETE.format(sep=general.SEPARATOR, data='\n  •'.join(delete_list)),
            button_generator(
                delete_list
            ),
            DeleteStates.waiting_for_deletion_data_type
        )

    elif date in instance.data_list:
        await queries.delete_daily_data(instance.user_id, date)
        return (
            f"{general.DATA_IS_DELETED}\n{general.INPUT_START}",
            ReplyKeyboardRemove(),
            States.clear
        )
    else:
        return (
            general.INCORRECT_INPUT + "За какую дату вы хотите удалить данные?",
            button_generator(instance.data_list),
            None
        )


def delete_element(element, instance):

    stage = instance.survey_stage
    const = import_loader.get_constants(stage)

    if element == "отменить":
        message_answer = renderers.render_list_or_dict(
            instance.current_data, stage, instance.positions_products
        )
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation

    elif element in instance.current_data_list:
        instance.current_data_list.remove(element)

        if stage in (2, 9, 11, 13, 15):
            instance.data_list.append(element)

        elif stage == 3:
            position = list(instance.data_dict.keys())[instance.count]
            instance.data_dict[position] = instance.current_data_list.copy()
            instance.current_position_for_change = None
            instance.current_data_list = []

        message_answer = const.ITEM_DELETED.format(
            item=element
        ) + renderers.render_list_or_dict(
            instance.current_data, stage, instance.positions_products
        )
        buttons = buttons_yes_or_not()
        next_state = FillingStates.waiting_for_data_confirmation

    else:
        message_answer = const.DONT_EXIST + const.ASK_NAME_FOR_DELETE
        buttons = button_generator(instance.current_data_list)
        next_state = None

    return (message_answer, buttons, next_state)
