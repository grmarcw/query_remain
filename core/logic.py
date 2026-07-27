def show_recipes(recipes):

    result = []
    for position, data in recipes.items():
        result.append(f"{position}:")
        for ingredient, quantity in data.items():
            result.append(f"    {ingredient}: {quantity}")

    return "\n".join(result)
