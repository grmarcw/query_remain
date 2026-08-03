import pytest

from bot.states_fsm import FillingStates, DeleteStates, ChangingData, States
from core import check_data
from constants import constants_for_tests as t, constants


@pytest.mark.asyncio
async def test_check_data_in_db_not_exist(mock_not_exist_db_data,
                                    instance_stage_one,
                                    mock_ask_ingredient,
                                    mock_delete_kb):
    result_not_exist = await check_data.check_data_in_db(instance_stage_one)
    assert result_not_exist == (t.ASK_INGREDIENT,
                                t.DELETE_KB,
                                FillingStates.waiting_for_data_list)

@pytest.mark.asyncio
async def test_check_data_in_db_exist(instance_stage_one,
                                      mock_exist_db_data,
                                      mock_buttons_show_delete,
                                      mock_exist_delivery_data):
    result_exist = await check_data.check_data_in_db(instance_stage_one)
    assert result_exist == (constants.ASK_SHOW_DELETE,
                            t.BUTTONS_SHOW_DELETE,
                            DeleteStates.waiting_for_delete_or_display)


def test_give_response_text_for_check_correctness_data(instance_stage_one,
                                                       instance_stage_two,
                                                       instance_stage_three,
                                                       mock_ask_position,
                                                       mock_delete_kb,
                                                       mock_button_choose,
                                                       mock_choose_position,
                                                       mock_ask_quantity,
                                                       mock_button_generator,
                                                       mock_buttons_yes_not):

    result_yes_stage_one = check_data.give_response_text_for_check_correctness_data(
        'да', instance_stage_one
    )
    result_no_stage_one = check_data.give_response_text_for_check_correctness_data(
        'нет', instance_stage_one
    )
    result_yes_stage_two = check_data.give_response_text_for_check_correctness_data(
        'да', instance_stage_two
    )
    result_no_stage_two = check_data.give_response_text_for_check_correctness_data(
        'нет', instance_stage_two
    )
    result_yes_stage_three = check_data.give_response_text_for_check_correctness_data(
        'да', instance_stage_three
    )
    result_no_stage_three = check_data.give_response_text_for_check_correctness_data(
        'нет', instance_stage_three
    )
    result_else = check_data.give_response_text_for_check_correctness_data(
        'что-то', instance_stage_one
    )
    assert result_yes_stage_one == (t.ASK_PRODUCT,
                                    t.DELETE_KB,
                                    FillingStates.waiting_for_data_for_composition)
    assert result_no_stage_one == (t.CHOOSE_POSITION,
                                   t.BUTTON_CHOOSE,
                                   ChangingData.waiting_result_choosing_action)
    assert result_yes_stage_two == (t.QUANTITY,
                                    t.DELETE_KB,
                                    FillingStates.waiting_quantity)
    assert result_no_stage_two == (constants.ASK_POSITION_FOR_CHANGE,
                                   t.BUTTON_GENERATOR,
                                   ChangingData.waiting_ingredient_name)
    assert result_yes_stage_three == (constants.CONFIRM_SAVING,
                                      t.BUTTONS_YES_NOT,
                                      States.waiting_save_confirmation)
    assert result_no_stage_three == (constants.ASK_PRODUCT_FOR_CHANGE,
                                     t.BUTTON_GENERATOR,
                                     ChangingData.waiting_position_name_for_change)
    assert result_else == (constants.INPUT_YES_NO,
                           t.BUTTONS_YES_NOT,
                           FillingStates.waiting_for_data_confirmation)


def test_choose_action(instance_stage_one,
                       instance_stage_two,
                       mock_ask_position,
                       mock_button_generator,
                       mock_delete_kb,
                       mock_buttons_yes_not,
                       mock_render_list,
                       mock_render_dict,
                       mock_choose_position_str,
                       mock_button_choose,
                       mock_ask_position_wpii):

    actions = ("поменять позицию", "удалить позицию", "добавить позицию", "начать заполнение заново", "отменить")
    result_action_zero_stage_one = check_data.choose_action(
        actions[0], instance_stage_one
    )
    result_action_one_stage_one = check_data.choose_action(
        actions[1], instance_stage_one
    )
    result_action_two_stage_one = check_data.choose_action(
        actions[2], instance_stage_one
    )
    result_action_three_stage_one = check_data.choose_action(
        actions[3], instance_stage_one
    )
    result_action_four_stage_one = check_data.choose_action(
        actions[4], instance_stage_one
    )
    result_action_zero_stage_two = check_data.choose_action(
        actions[0], instance_stage_two
    )
    result_action_one_stage_two = check_data.choose_action(
        actions[1], instance_stage_two
    )
    result_action_two_stage_two = check_data.choose_action(
        actions[2], instance_stage_two
    )
    result_action_three_stage_two = check_data.choose_action(
        actions[3], instance_stage_two
    )
    result_action_four_stage_two = check_data.choose_action(
        actions[4], instance_stage_two
    )
    result_else = check_data.choose_action(
        'что-то', instance_stage_one
    )
    assert result_action_zero_stage_one == (constants.ASK_POSITION_FOR_CHANGE,
                                            t.BUTTON_GENERATOR,
                                            ChangingData.waiting_element_for_change)
    assert result_action_one_stage_one == (constants.ASK_POSITION_FOR_DELETE,
                                           t.BUTTON_GENERATOR,
                                           ChangingData.delete)
    assert result_action_two_stage_one == (constants.ASK_LIST_INGREDIENTS,
                                           t.DELETE_KB,
                                           ChangingData.add)
    assert result_action_three_stage_one == (constants.ASK_LIST_INGREDIENTS,
                                             t.DELETE_KB,
                                             FillingStates.waiting_for_data_list)
    assert result_action_four_stage_one == (t.LIST_TEXT,
                                            t.BUTTONS_YES_NOT,
                                            FillingStates.waiting_for_data_confirmation)
    assert result_action_zero_stage_two == (constants.ASK_PRODUCT_FOR_CHANGE,
                                            t.BUTTON_GENERATOR,
                                            ChangingData.waiting_element_for_change)
    assert result_action_one_stage_two == (constants.ASK_PRODUCT_FOR_DELETE,
                                           t.BUTTON_GENERATOR,
                                           ChangingData.delete)
    assert result_action_two_stage_two == (t.ASK_PRODUCT,
                                           t.DELETE_KB,
                                           ChangingData.add)
    assert result_action_three_stage_two == (t.ASK_PRODUCT,
                                             t.DELETE_KB,
                                             ChangingData.add)
    assert result_action_four_stage_two == (t.RENDER_DICT,
                                            t.BUTTONS_YES_NOT,
                                            FillingStates.waiting_for_data_confirmation)
    assert result_else == (f'{constants.INCORRECT_INPUT}\n{constants.CHOOSING_ACTION}',
                           t.BUTTON_CHOOSE,
                           None)

