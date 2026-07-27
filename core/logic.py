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
