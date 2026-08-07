from aiogram.types import KeyboardButton
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


def buttons_choose_action(filling_stage=1):
    bilder = ReplyKeyboardBuilder()
    if filling_stage == 1:
        item = 'позицию'
    elif filling_stage == 5:
        item = 'перемещение'
    else:
        item = 'поставщика'

    if filling_stage != 4 and filling_stage != 5:
        bilder.button(text=f"Поменять {item}")
    bilder.button(text=f"Удалить {item}")
    bilder.button(text=f"Добавить {item}")
    bilder.button(text="Начать заполнение заново")
    bilder.button(text="Отменить")

    bilder.adjust(2)
    kb = bilder.as_markup(resize_keyboard=True)

    return kb


def button_generator(some_list,list_for_append=[], without_cancel=False):
    builder = ReplyKeyboardBuilder()

    for i in some_list:
        builder.add(KeyboardButton(text=i))
    if list_for_append != []:
        for i in list_for_append:
            builder.add(KeyboardButton(text=i))

    if not without_cancel:
        builder.add(KeyboardButton(text="Отменить"))

    builder.adjust(3)
    kb = builder.as_markup(resize_keyboard=True)
    return kb
