from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    # состояния для работы с заполнением данных о рецептах
    waiting_ingredient_list = State()
    waiting_position_list = State()
    waiting_for_data_confirmation = State()
    waiting_position_list = State()


class DeleteFromDB(States):
    # состояния для удаления данных из бд
    waiting_for_change_decision_from_db = State()
    waiting_ans_about_delete_data_from_db = State()


class ChangingData(States):
    waiting_result_choosing_action = State()

    waiting_elem_for_change = State()
    change = State()
    delete = State()
    add = State()

    waiting_ingredient_name = State()
    waiting_choose_action = State()
    recomposition = State()
