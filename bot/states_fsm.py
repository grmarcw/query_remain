from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    # состояния для работы с заполнением данных о рецептах
    waiting_ingredient_list = State()


class DeleteFromDB(States):
    # состояния для удаления данных из бд
    waiting_for_change_decision_from_db = State()
    waiting_ans_about_delete_data_from_db = State()
