from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    waiting_ingredient_list = State()
    waiting_for_change_decision = State()