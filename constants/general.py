INPUT_START = f'{"="*20}\nНажмите /start'
CANCELED = "Операция отменена"
DELETED = "Данные удалены"
INPUT_YES_NO = 'Я не понимаю\nПожалуйста, введите "да" или "нет"'
INCORRECT_INPUT = f'Некорректный ввод\n{"-" * 5}\n'

CHECKING_CORRECTNESS = """Пожалуйста, проверьте корректность введенных данных

====================
{checking_data}
====================

Введенные данные корректны?
Напишите "да" или "нет"
"""

SEPARATOR = "=" * 20

SHOW_OR_DELETE = "Хотите отобразить данные или удалить?"

INPUT_DATA_FOR_DELETE = """Выберите какие данные хотите удалить
{sep}
{data}"""


FILLED_RECIPES_DATA = "Данные о рецептах заполнены\n"
FILLED_DELIVERY_DATA = "Данные о поставках заполнены\n"
FILLED_BALANCE_DATA = "Данные о начальном остатке продукции заполнены\n"

CONFIRM_SAVING = "Подтвердите сохранение данных"
SHOW_SAVING_DATA = "Сохранены следующие данные:\n{data}\n----\nДля продолжения ввода первичных данных, нажмите /start"

DATE_CLARIFICATION = "Вы хотите заполнить данные за {date}?"
INPUT_CORRECT_DATE = (
    "Пожалуйста, напишите дату для заполнения данных в формате DD.MM.YYYY"
)
INPUT_CORRECT_FORMAT = "Введите дату в формате DD.MM.YYYY"

OPERATION_CANCEL = "Операция отменена\n/start"
DATA_IS_DELETED = "Данные удалены\n/start"
