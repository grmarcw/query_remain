def format(instance, data_from_db):
    products_list = []
    deliveries_data = data_from_db.deliveries
    positions = []

    for product, recipe in data_from_db.recipes.items():
        products_list.append(product)
        for position in recipe.keys():
            if position not in positions:
                positions.append(position)

    if data_from_db.positions_products:
        products_list.extend(data_from_db.positions_products)
        positions.extend(data_from_db.positions_products)

    products_list.sort()
    positions.sort()
    instance.data_list = products_list
    instance.products = products_list
    instance.deliveries = deliveries_data
    instance.positions = positions

    return instance
