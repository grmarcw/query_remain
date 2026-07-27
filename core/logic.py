import constants


def show_recipes(recipes):

    result = []
    for position, data in recipes.items():
        result.append(f"{position}:")
        for ingredient, quantity in data.items():
            result.append(f"    {ingredient}: {quantity}")

    return "\n".join(result)

def convert_string_to_list(string_for_convert):
    result = [
        element.strip(" ")
        for element in string_for_convert.lower().split(",")
        if element.strip()
    ]
    return result

def render_list(list_for_output, sep=constants.SEPARATOR):
    str_for_output = "Вы хотите отслеживать следующие позиции:\n\n•{list_}\n"
    return constants.CHECKING_CORRECT_DATA.format(
        sep=sep,
        checking_data=str_for_output.format(
            list_="\n•".join(list_for_output)
        ),
    )

def render_dict(ingredients_positions, sep=constants.SEPARATOR, option=1):
    ingredients_list = []
    positions = []
    some = []
    some_two = []

    for k, v in ingredients_positions.items():
        ingredients_list.append(k)
        positions.append(v)
    for i, ingred in enumerate(ingredients_list):
        some.append(
            constants.POSITION_LIST.format(
                ingredient=ingred.upper(), positions="\n•".join(positions[i])
            )
        )
        some_two.append(f'Позиция:\n"{ingred.upper()}"\nТовары, в которые она входит:\n{"\n".join(positions[i])}\n{sep}\n')

    if option == 1:
        return constants.CHECKING_CORRECT_DATA.format(sep=sep, checking_data="\n".join(some))
    else:
        return "\n".join(some_two)

