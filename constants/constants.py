ASK_LIST_INGREDIENTS =  "Какие позиции вы хотите отслеживать?\nНапишите все названия через запятую"

ASK_DELIVERIES_LIST = "Каких поставщиков вы хотите отслеживать?\nНапишите все названия через запятую"

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

ASK_COMPOSITION_DELIVERY = 'В какую поставку идет позиция "{position}"?'

POSITION_LIST = "{ingredient} идет в:\n•{positions}\n"

choose = "\n{sep}\n•Поменять {item}\n•Удалить {item}\n•Добавить {item}\n•Начать заполнение заново"
CHOOSING_ACTION = choose.format(sep=SEPARATOR, item='позицию')
CHOOSING_ACTION_DELIVERY = choose.format(sep=SEPARATOR, item='поставщика')
CHOOSING_ACTION_DELIVERY_ADD_DELETE = f"\n{"=" * 20}\n•Удалить поставку\n•Добавить поставку\n•Начать заполнение заново"
CHOOSING_ACTION_SHIPMENT_ADD_DELETE = f"\n{"=" * 20}\n•Удалить перемещение\n•Добавить перемещение\n•Начать заполнение заново"

POSITION_DONT_EXIST = '''Такой позиции не существует
Пожалуйста, выбери какую позицию ты хочешь изменить:
•{data_for_changing}'''
DELIVERIER_DONT_EXIST = '''Такого поставщика не существует
Пожалуйста, выбери какого поставщика ты хочешь изменить:
•{data_for_changing}'''
PRODUCT_DONT_EXIST = '''Нет такого товара/позиции
Пожалуйста введи позицию, в которой хочешь внести изменения из списка ниже:
•{data_for_changing}'''

INPUT_NEW_NAME = "Введите новое название"

CHOOSE_POSITION_FOR_CHANGE = '''Что вы хотите изменить?
{sep}
Выберите и напишите одно действие:
{choose_list}'''

ASK_QUANTITY = '''Сколько ингридиента "{ingr}" идет в товар "{product}"?
Пожалуйста, укажите в ГРАММАХ'''

ask_change = "В как{item} вы хотите внести изменения?"
ASK_POSITION_FOR_CHANGE = ask_change.format(item='ой позиции')
ASK_PRODUCT_FOR_CHANGE = ask_change.format(item='ом товаре')
ASK_DELIVERIER_FOR_CHANGE = ask_change.format(item='ом поставщике')

ask_delete = "Как{item} вы хотите удалить?"
ASK_POSITION_FOR_DELETE = ask_delete.format(item='ую позицию')
ASK_PRODUCT_FOR_DELETE = ask_delete.format(item='ой товар')
ASK_DELIVERIER_FOR_DELETE = ask_delete.format(item='ого поставщика')
ASK_SHIPMENT_FOR_DELETE = ask_delete.format(item='ое перемещение')


SHOW_OR_DELETE = "Хотите отобразить данные или удалить?"

INPUT_DATA_FOR_DELETE = '''Выберите какие данные хотите удалить
{sep}
{data}'''

POSITION_IS_DELETED = 'Позиция "{position}" удалена\n'
PRODUCT_IS_DELETED = 'Товар "{product}" удален\n'
DELIVERIER_IS_DELETED = 'Поставщик "{position}" удален\n'
SHIPMENT_IS_DELETED = 'Позиция "{position}" удалена из перемещений\n'



INPUT_START = f'{"="*20}\nНажмите /start'
OPERATION_CANCEL = 'Операция отменена'
DATA_IS_DELETED = 'Данные удалены'
INPUT_YES_NO = 'Я не понимаю\nПожалуйста, введите "да" или "нет"'
INCORRECT_INPUT = '''Некорректный ввод'''


CONFIRM_SAVING = "Подтвердите сохранение данных"
SHOW_SAVING_DATA = 'Сохранены следующие данные:\n{data}'

ASK_FILLING_DATA_AGAIN = 'Хотите заполнить данные заново?'


ASK_QUANTITY_BALANCE = 'Какой текущий остаток позиции "{position}"?\nПожалуйста, укажите в кг/л'
INPUT_NEW_QUANTITY = 'Введите корректное значение текущего остатка для позиции {position}'


DATE_CLARIFICATION = 'Вы хотите заполнить данные за {date}?'
INPUT_CORRECT_DATE = 'Пожалуйста, напишите дату для заполнения данных в формате DD.MM.YYYY'
INPUT_CORRECT_FORMAT = 'Введите дату в формате DD.MM.YYYY'


INPUT_SOLD_PRODUCT_QUANTITY = 'Сколько продано\n{product}?'

INPUT_DELIVERIES_NAMES = 'Какие поставки были в этот день?'
INPUT_OTHER_DELIVERIES = 'Какие еще поставки были?'

NO_MORE = 'больше поставок не было'
NO_MORE_SHIPMENT = 'больше перемещений не было'

DELIVERIER_DONT_EXIST_WITHOUT_FORMAT = 'Такого поставщика не существует\nПожалуйста введите существующуего поставщика'

SHIPMENT_CONFIRM = 'Какие позиции были перемещены С других точек на вашу?'
SHIPMENT_CONFIRM_OUT = 'Какие позиции были перемещены НА другие точки с вашей?'
INPUT_OTHER_SHIPMENT = 'Какие еще позиции были перемещены?'

