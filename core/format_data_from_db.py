def format(instance, data_from_db):
    products_list = []
    deliveries_data = data_from_db.deliveries
    positions = []

    for product, recipe in data_from_db.recipes.items():
        products_list.append(product)
        for position in recipe.keys():
            if position not in positions:
                positions.append(position)

    products_list.sort()
    positions.sort()
    instance.products = products_list
    instance.delivery = deliveries_data
    instance.positions = positions

    return instance