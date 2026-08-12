from sqlalchemy.util import format_argspec_plus


def get_actual_balance(data, instance):
    recipes = instance.recipes
    daily_datas = data
    start_balance = instance.data_dict
    finish_balance = {}

    products_for_plus = {}
    products_for_minus = {}

    for product, recipe in recipes.items():
        for position, quantity in recipe.items():
            recipes[product][position] = float(quantity) / 1000

    for day_data in daily_datas:
        for date, data in day_data.items():
            for name_column, data_column in data.items():
                for product, quantity in data_column.items():
                    quantity = float(quantity)
                    products_for_plus.setdefault(product, 0)
                    products_for_minus.setdefault(product, 0)
                    if name_column in ('поставки', 'перемещения с других точек'):
                        products_for_plus[product] += quantity
                    elif name_column in ('проданная продукция', 'перемещения на другие точки', 'списания'):
                        products_for_minus[product] += quantity

    positions_for_plus = {}
    positions_for_minus = {}

    for k,v in products_for_plus.items():
        if k in recipes:
            for product, recipe in recipes.items():
                if k == product:
                    for ingredients, quantity in recipe.items():
                        quantity = float(quantity)
                        positions_for_plus.setdefault(ingredients, 0)
                        positions_for_plus[ingredients] += quantity * v

        else:
            positions_for_plus.setdefault(k, 0)
            positions_for_plus[k] += v


    for k,v in products_for_minus.items():
        if k in recipes:
            for product, recipe in recipes.items():
                if k == product:
                    for ingredients, quantity in recipe.items():
                        quantity = float(quantity)
                        positions_for_minus.setdefault(ingredients, 0)
                        positions_for_minus[ingredients] += quantity * v

        else:
            positions_for_minus.setdefault(k, 0)
            positions_for_minus[k] += v


    for product, start_quantity in start_balance.items():
        start_quantity = float(start_quantity)
        finish_balance.setdefault(product, start_quantity)

    for product_finish, quantity in finish_balance.items():
        for product_for_minus, quantity_for_minus in positions_for_minus.items():
            if product_finish == product_for_minus:
                finish_balance[product_finish] -= float(quantity_for_minus)



        for product_for_plus, quantity_for_plus in positions_for_plus.items():
                if product_finish == product_for_plus:
                    finish_balance[product_finish] += quantity_for_plus

    for position, quantity in finish_balance.items():
        finish_balance[position] = round(quantity, 3)

    return finish_balance

