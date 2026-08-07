from datetime import date, datetime

from aiogram.types import ReplyKeyboardRemove

from bot.buttons import buttons_yes_or_not
from bot.states_fsm import CheckDate, States, Main
from constants import constants
from core import format_data_from_db
from database import queries


def clarification(instance):
    date_today = date.today()
    output = date_today.strftime('%d.%m.%Y')
    instance.date = output

    return (
        constants.DATE_CLARIFICATION.format(date=output),
        buttons_yes_or_not(),
        CheckDate.waiting_for_confirm_date
    )

async def handle_date_confirmation(user_answer, instance):
    if user_answer == 'да':
        data_from_db = await queries.get_user_data(instance.id_user)
        format_data_from_db.format(instance, data_from_db)
        return (
            constants.INPUT_SOLD_PRODUCT_QUANTITY.format(product=instance.products[0]),
            ReplyKeyboardRemove(),
            Main.waiting_for_quantity_sold
        )
    elif user_answer == 'нет':
        return (
            constants.INPUT_CORRECT_DATE,
            ReplyKeyboardRemove(),
            CheckDate.waiting_for_correct_date
        )
    else:
        return (
            constants.INPUT_YES_NO,
            buttons_yes_or_not(),
            None
        )

def ask_correct_date(user_answer, instance):
    try:
        date = datetime.strptime(user_answer,'%d.%m.%Y')
        date = date.strftime('%d.%m.%Y')
        instance.date = date
        return (
            constants.DATE_CLARIFICATION.format(date=date),
            buttons_yes_or_not(),
            CheckDate.waiting_for_confirm_date
        )
    except ValueError:
        return (
            f'{constants.INCORRECT_INPUT}\n{constants.INPUT_CORRECT_FORMAT}',
            ReplyKeyboardRemove(),
            None
        )
