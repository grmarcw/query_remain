from constants import general


def convert_string_to_list(string_for_convert):
    result = [
        element.strip(" ")
        for element in string_for_convert.lower().split(",")
        if element.strip()
    ]
    return result


def render_list_or_dict(data, stage=1, list_for_add=None, option=1):
    # option == 1 -> для подтверждения корректности
    # option == 2 -> для вывода данных без доп. строк
    # option == 67 -> для показа данных из бд, исп. в случае заполненности данных positions_products
    if stage == 1:
        if data == []:
            str_for_output = "Вы не ввели позиции для отслеживания"
        else:
            str_for_output = "Вы хотите отслеживать следующие позиции:\n\n•{list_}\n"
            str_for_output = str_for_output.format(list_="\n•".join(data))

    elif stage == 2:
        if data == []:
            str_for_output = "Среди позиций нет товаров"
        else:
            str_for_output = "Следующие позиции являются товарами:\n\n•{list_}\n"
            str_for_output = str_for_output.format(list_="\n•".join(data))

    elif stage == 3:
        # data ->  {position: [products]}
        positions_list = []
        products_list = []

        list_for_output = []

        for position, products in data.items():
            positions_list.append(position)
            products_list.append(products)
        for index, position in enumerate(positions_list):
            list_for_output.append(
                f'•{position}:\n  -{"\n  -".join(products_list[index])}'
            )

        if list_for_add:
            list_for_output.append(
                f'\n----\nЯвляются товарами\n----\n{"\n".join(list_for_add)}'
            )
        str_for_output = "\n".join(list_for_output)

    elif stage == 4 or stage == 10:
        result = []
        for position, data in data.items():
            result.append(f"•{position}:")
            for ingredient, quantity in data.items():
                result.append(f"   -{ingredient}: {quantity}")

        str_for_output = "\n".join(result)

    elif stage == 5:
        if data == []:
            str_for_output = "Вы не ввели поставщиков для отслеживания"
        else:
            str_for_output = (
                "Вы хотите отслеживать следующих поставщиков:\n\n•{list_}\n"
            )
            str_for_output = str_for_output.format(list_="\n•".join(data))

    elif stage == 6:
        list_for_output = []
        for deliverier, positions in data.items():
            list_for_output.append(f'{deliverier}:\n   •{"\n   •".join(positions)}')

        str_for_output = "\n".join(list_for_output)

    elif stage in (7, 8, 12, 14, 16):
        list_for_output = []

        for position, quantity in data.items():
            list_for_output.append(f"{position}:  {quantity}")

        str_for_output = "\n".join(list_for_output)

    elif stage == 9:
        if data == []:
            str_for_output = "Поставок не было"
        else:
            str_for_output = "В этот день были следующие поставки:\n\n•{list_}\n"
            str_for_output = str_for_output.format(list_="\n•".join(data))

    elif stage == 11:
        if data == []:
            str_for_output = "Перемещений с других точек не было"
        else:
            str_for_output = (
                "В этот день были следующие перемещения с других точек:\n\n•{list_}\n"
            )
            str_for_output = str_for_output.format(list_="\n•".join(data))

    elif stage == 13:
        if data == []:
            str_for_output = "Перемещений на другие точки не было"
        else:
            str_for_output = (
                "В этот день были следующие перемещения на другие точки:\n\n•{list_}\n"
            )
            str_for_output = str_for_output.format(list_="\n•".join(data))

    elif stage == 15:
        if data == []:
            str_for_output = "Списаний не было"
        else:
            str_for_output = "В этот день были следующие списания:\n\n•{list_}\n"
            str_for_output = str_for_output.format(list_="\n•".join(data))

    elif stage == 17:
        list_for_output = []

        for date, data_ in data.items():
            list_for_output.append(
                f'"дата": {date}\n'
            )
            for name_column, data_dict in data_.items():
                list_for_output.append(f'\n----\n{name_column}:\n----\n')
                if data_dict:
                    for product, quantity in data_dict.items():
                        list_for_output.append(
                            f'{product}:  {quantity}'
                        )
                else:
                    list_for_output.append('нет')

        str_for_output = "\n".join(list_for_output)

    elif stage == 18:
        list_for_output = []
        for dictionary in data:
            for date, dict_data in dictionary.items():
                list_for_output.append(
                    f'дата: {date}\n'
                )
                for name_column, data_from_column in dict_data.items():
                    list_for_output.append(f'\n----\n{name_column}:\n----\n')
                    if data_from_column:
                        for product, quantity in data_from_column.items():
                            list_for_output.append(
                                f'{product}:  {quantity}'
                            )
                    else:
                        list_for_output.append('нет')

        str_for_output = "\n".join(list_for_output)

    if option == 1:
        return general.CHECKING_CORRECTNESS.format(checking_data=str_for_output)
    elif option == 2:
        if stage in (1, 2):
            return f"•{'\n•'.join(data)}"
        else:
            return str_for_output

    elif option == 67:
        return f'\n----\nЯвляются товарами\n----\n{"\n".join(data)}'
