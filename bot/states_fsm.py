from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    # состояния для сохранения данных
    waiting_save_confirmation = State()
    clear = State()

class DeleteStates(States):
    # состояния для удаления данных
    waiting_for_delete_or_display = State()
    waiting_for_deletion_data_type = State()

class FillingStates(States):
# состояния для работы с заполнением данных о рецептах
    waiting_for_data_list = State()
    waiting_for_data_for_composition = State()
    waiting_quantity = State()

    waiting_for_data_confirmation = State()

    waiting_for_delivery_data_composition = State()
    waiting_for_filling_data_confirmation = State()


class ChangingData(States):
    waiting_result_choosing_action = State()

    waiting_element_for_change = State()
    change = State()
    delete = State()
    add = State()

    waiting_ingredient_name = State()
    waiting_choose_action = State()
    recomposition = State()

    waiting_position_name_for_change = State()
    waiting_new_quantity = State()

class CurrentActualBalance(States):
    waiting_for_quantity = State()

class CheckDate(States):
    waiting_for_confirm_date = State()

    waiting_for_correct_date = State()
