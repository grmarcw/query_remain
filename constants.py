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

POSITION_LIST = "{ingredient} идет в:\n•{positions}\n"

choose = "\n{sep}\n•Поменять позицию\n•Удалить позицию\n•Добавить позицию\n•Начать заполнение заново"
CHOOSING_ACTION = choose.format(sep=SEPARATOR)
