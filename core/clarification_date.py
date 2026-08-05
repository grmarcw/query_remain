from datetime import date, datetime

from aiogram.types import ReplyKeyboardRemove

from bot.buttons import buttons_yes_or_not
from bot.states_fsm import CheckDate, States
from constants import constants


def clarification(instance):
    date_today = date.today()
    output = date_today.strftime('%d.%m.%Y')
    instance.date = output

    return (
        constants.DATE_CLARIFICATION.format(date=output),
        buttons_yes_or_not(),
        CheckDate.waiting_for_confirm_date
    )

def handle_date_confirmation(user_answer, instance):

    if user_answer == 'да':
        return (
            None,
            None,
            None
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
