from typing import List, Dict

class InitialData:
    id_user: int = None
    ingredients: List[str] = []                  # список отслеживаемых ингредиентов или поставщиков
    recipes: Dict[str, dict] = {}                # словарь {товар:{ингредиент: количество}}
    compositions: Dict[str, list] = {}           # словарь {отслеживаемый ингредиент: [список, из, товаров]}
    survey_stage: int = 1                        # текущий этап заполнения данных
    product_is_ingredient: List[str] = []        # список ингредиентов, которые являются товарами
    ingredients_without_products: List[str] = []
    count:int = 0           # универсальный счетчик
    idx_ing: int = 0        # индекс ингридиента
    idx_prd: int = 0        # индекс продукта
    cpl: List[str] = []     # текущий список продуктов для изменения
    cil: List[str] = []     # текущий список ингридиентов для изменения
    cifc: str = None        # текущий ингридиент для изменения
    pfc: str = None         # текущая позиция для изменения
    data_filling_stage: int = 1      # текущий этап заполнения данных (рецепты или поставки)
    deliveries: Dict[str, list] = {} # данные о поставщках

    full_ingredients_list: List[str] = [] #список ингридиентов

class DailyData:
    id_user: int = None
    date: str = None
