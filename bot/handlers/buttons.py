from aiogram.utils.keyboard import ReplyKeyboardBuilder


def buttons_show_delete():
    builder = ReplyKeyboardBuilder()

    builder.button(text="Удалить данные")
    builder.button(text="Отобразить данные")

    builder.adjust(2)
    kb = builder.as_markup(resize_keyboard=True)
    return kb


def buttons_yes_or_not():
    builder = ReplyKeyboardBuilder()

    builder.button(text="да")
    builder.button(text="нет")

    builder.adjust(2)
    kb = builder.as_markup(resize_keyboard=True)
    return kb

def buttons_choose_action():
    bilder = ReplyKeyboardBuilder()
    bilder.button(text='Поменять позицию')
    bilder.button(text='Удалить позицию')
    bilder.button(text='Добавить позицию')
    bilder.button(text='Начать заполнение заново')
    bilder.button(text='Отменить')

    bilder.adjust(2)
    kb = bilder.as_markup(resize_keyboard=True)

    return kb
