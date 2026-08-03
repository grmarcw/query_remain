from typing import List, Dict

class RecipesData:
    id_user: int = None
    ingredients: List[str] = None
    recipes: Dict[str, dict] = None
    compositions: Dict[str, list] = None
    survey_stage: int = None
    product_is_ingredient: Dict[str] = None
    ingredients_without_products: List[str] = None
    count:int = None
    idx_ing: int = None
    idx_prd: int = None
    cpl: List[str] = None
    cil: List[str] = None
    cifc: str = None
    pfc: str = None