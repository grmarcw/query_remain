from typing import List, Dict

class InitialData:
    def __init__(self):
        self.id_user: int = None
        self.ingredients: List[str] = []                  # список отслеживаемых ингредиентов или поставщиков
        self.recipes: Dict[str, dict] = {}                # словарь {товар:{ингредиент: количество}}
        self.compositions: Dict[str, list] = {}           # словарь {отслеживаемый ингредиент: [список, из, товаров]}
        self.survey_stage: int = 1                        # текущий этап заполнения данных
        self.product_is_ingredient: List[str] = []        # список ингредиентов, которые являются товарами
        self.ingredients_without_products: List[str] = []
        self.count:int = 0           # универсальный счетчик
        self.idx_ing: int = 0        # индекс ингридиента
        self.idx_prd: int = 0        # индекс продукта
        self.cpl: List[str] = []     # текущий список продуктов для изменения
        self.cil: List[str] = []     # текущий список ингридиентов для изменения
        self.cifc: str = None        # текущий ингридиент для изменения
        self.pfc: str = None         # текущая позиция для изменения
        self.data_filling_stage: int = 1      # текущий этап заполнения данных (рецепты или поставки)
        self.deliveries: Dict[str, list] = {} # данные о поставщках

        self.full_ingredients_list: List[str] = [] #список ингридиентов
        self.filling_stage = 1

class DailyData:
    def __init__(self):
        self.id_user: int = None
        self.date: str = None
        self.products = []
        self.positions = []
        self.delivery = {}
        self.compositions = {}

        self.filling_stage = 2
        self.count = 0

        self.survey_stage = 0
        self.data_filling_stage = 0

        self.cpfc = None
        
        self.deliveries_in_date = []
        self.shipment_in_date = []
        self.shipment_out_in_date = []
