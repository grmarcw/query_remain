from constants import constants


def show_recipes(recipes):

    result = []
    for position, data in recipes.items():
        result.append(f"•{position}:")
        for ingredient, quantity in data.items():
            result.append(f"   -{ingredient}: {quantity}")

    return "\n".join(result)


def convert_string_to_list(string_for_convert):
    result = [
        element.strip(" ")
        for element in string_for_convert.lower().split(",")
        if element.strip()
    ]
    return result


def render_list(list_for_output, stage=1 ):

    if stage == 1:
        str_for_output = "Вы хотите отслеживать следующие позиции:\n\n•{list_}\n"
    elif stage == 2:
        str_for_output = "Вы хотите отслеживать следующих поставщиков:\n\n•{list_}\n"
    elif stage == 3:
        if list_for_output == []:
            str_for_output = 'Поставок в этот день не было'
        else:
            str_for_output = "В этот день призжали следующие поставки:\n\n•{list_}\n"
    elif stage == 4:
        if list_for_output == []:
            str_for_output = 'Перемещений в этот день не было'
        else:
            str_for_output = "В этот день были следующие перемещения:\n\n•{list_}\n"
    return constants.CHECKING_CORRECT_DATA.format(
        sep=constants.SEPARATOR,
        checking_data=str_for_output.format(list_="\n•".join(list_for_output)),
    )


def render_dict(
    ingredients_positions, list_for_add=None, option=1, stage=1
):
    ingredients_list = []
    positions = []
    some = []
    some_two = []
    some_three = []

    for k, v in ingredients_positions.items():
        ingredients_list.append(k)
        positions.append(v)
    for i, ingred in enumerate(ingredients_list):
        some.append(
            constants.POSITION_LIST.format(
                ingredient=ingred.upper(), positions="\n•".join(positions[i])
            )
        )
        if stage == 1:
            some_two.append(
                f'Позиция:\n"{ingred.upper()}"\nТовары, в которые она входит:\n{"\n".join(positions[i])}\n{constants.SEPARATOR}\n'
            )
        else:
            some_two.append(
                f'•"{ingred.upper()}"\n  -{"\n  -".join(positions[i])}\n{constants.SEPARATOR}\n'
            )
            some_three.append(
                f'•{ingred}:\n    -{"\n    -".join(positions[i])}\n'
            )
    if list_for_add:
        some.append(f'\n----\nЯвляются товарами\n----\n{"\n".join(list_for_add)}')
    if option == 1:
        return constants.CHECKING_CORRECT_DATA.format(
            sep=constants.SEPARATOR, checking_data="\n".join(some)
        )
    elif option == 2:
        return "\n".join(some_two)
    else:
        return "\n".join(some_three)


def render_dict_balance(dict, option=1):
    list_for_render = []
    for position, actual_balance in dict.items():
        list_for_render.append(
            f'{position}: {actual_balance}'
        )
    if option == 1:
        return constants.CHECKING_CORRECT_DATA.format(
            sep=constants.SEPARATOR, checking_data="\n".join(list_for_render)
        )
    elif option == 2:
        return "\n".join(list_for_render)

