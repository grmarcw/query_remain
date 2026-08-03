def nest_dict(some_dictionary:dict):
    '''
    создает вложенный словарь из словаря,
    где ключ-строка, а значение-список
    :param some_dictionary: словарь для преобразования
    :return: вложенный словарь
    '''

    dict_for_return = {}

    for k_str, v_list in some_dictionary.items():
        for element in v_list:
            dict_for_return.setdefault(element, {})
            dict_for_return[element].setdefault(k_str, 0)

    return dict_for_return
