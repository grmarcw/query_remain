ASK_LIST_INGREDIENTS = (
    "Какие позиции вы хотите отслеживать\nНапишите название всех позиций через запятую"
)

CHECKING_CORRECT_DATA = """Пожалуйста, проверьте корректность введенных данных
{sep}
{checking_data}
{sep}
Введенные данные корректны?
Напишите "да" или "нет"
"""

SEPARATOR = "=" * 20

ASK_LIST_POSITIONS = 'В какие товары идет "{ingredient}"?\nНапишите все названия через запятую\n----\nЕсли позиция является товаром, напишите "{ingredient}"'
ASK_LIST_POSITIONS_WITHOUT_PRD_IS_ING = 'В какие товары идет "{ingredient}"?\nНапишите все названия через запятую'

POSITION_LIST = "{ingredient} идет в:\n•{positions}\n"

choose = "\n{sep}\n•Поменять позицию\n•Удалить позицию\n•Добавить позицию\n•Начать заполнение заново"
CHOOSING_ACTION = choose.format(sep=SEPARATOR)

POSITION_DONT_EXIST = '''Такой позиции не существует
Пожалуйста, выбери какую позицию ты хочешь изменить:
•{data_for_changing}'''

INPUT_NEW_NAME = "Введите новое название для позиции"

CHOOSE_POSITION_FOR_CHANGE = '''Что вы хотите изменить?
{sep}
Выберите и напишите одно действие:
{choose_list}'''

ASK_QUANTITY = '''Сколько ингридиента "{ingr}" идет в товар "{product}"?
Пожалуйста, укажите в ГРАММАХ'''

ASK_POSITION_FOR_CHANGE = "В какой позиции вы хотите внести изменения?"
ASK_POSITION_FOR_DELETE = "Какую позицию вы хотите удалить?"


PRODUCT_DONT_EXIST = '''Нет такого товара/позиции
Пожалуйста введи позицию, в которой хочешь внести изменения из списка ниже:
•{list_change}'''

INCORRECT_INPUT = '''Некорректный ввод'''

ASK_SHOW_DELETE = 'В базе найдены данные\nХотите отобразить данные или удалить?'
SHOW_OR_DELETE = "Хотите отобразить данные или удалить?"

CONFIRM_SAVING = "Подтвердите сохранение данных"

ASK_PRODUCT_FOR_CHANGE = "В каком товаре вы хотите внести изменения?"
ASK_PRODUCT_FOR_DELETE = "Какой товар вы хотите удалить?"

INPUT_YES_NO = 'Я не понимаю\nПожалуйста, введите "да" или "нет"'

INPUT_DATA_FOR_DELETE = '''Выберите какие данные хотите удалить
{sep}
{data}'''

INPUT_START = f'{"="*20}\nНажмите /start'

OPERATION_CANCEL = 'Операция отменена'
DATA_IS_DELETED = 'Данные удалены'

POSITION_IS_DELETED = 'Позиция {position} удалена'
PRODUCT_IS_DELETED = 'Товар {product} удален'

SHOW_SAVING_DATA = 'Сохранены следующие данные:\n{data}'
