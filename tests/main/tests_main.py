import pytest

import constants
from bot.states_fsm import FillingStates, States
from core import main
from constants import constants_for_tests as t, constants

def test_get_composition(instance_zero,
                         instance_one,
                         instance_two,
                         mock_ask_positions,
                         mock_delete_kb,
                         mock_buttons_yes_not,
                         mock_render_dict):
    result_zero = main.get_composition('боул', instance_zero)
    result_one = main.get_composition('капучино, Латте', instance_one)
    result_two = main.get_composition('капучино, Латте', instance_two)

    assert result_zero == (constants.CONFIRM_SAVING,
                           t.BUTTONS_YES_NOT,
                           States.waiting_save_confirmation)
    assert instance_zero.ingredients_without_products == []
    assert instance_zero.product_is_ingredient == ['боул']
    assert result_one == (t.ASK_PRODUCT,
                          t.DELETE_KB,
                          None)
    assert result_two == (t.RENDER_DICT,
                          t.BUTTONS_YES_NOT,
                          FillingStates.waiting_for_data_confirmation)
    assert instance_two.survey_stage == 2
    assert instance_one.ingredients_without_products == ['молоко', 'зерно', 'боул']
    assert instance_two.ingredients_without_products == ['молоко']


def test_get_quantity_ingredients(instance_three,
                                  instance_four,
                                  instance_five,
                                  mock_delete_kb,
                                  mock_buttons_yes_not,
                                  mock_ask_quantity,
                                  mock_check_correctness):
    result_incorrect = main.get_quantity_ingredients('one', instance_four)
    result_one = main.get_quantity_ingredients(6767, instance_four)
    result_two = main.get_quantity_ingredients(67, instance_three)
    result_three = main.get_quantity_ingredients(67, instance_five)

    assert result_incorrect == (f'{constants.INCORRECT_INPUT}\n{t.QUANTITY}',
                                t.DELETE_KB,
                                None)
    assert result_one == (t.QUANTITY,
                          t.DELETE_KB,
                          None)
    assert instance_four.recipes == {'капучино': {'молоко': 6767, 'зерно': 0}}
    assert result_two == (t.QUANTITY,
                          t.DELETE_KB,
                          None)
    assert instance_three.idx_ing == 0
    assert instance_three.idx_prd == 1
    assert result_three == (t.CHECKING_CORRECTNESS,
                            t.BUTTONS_YES_NOT,
                            FillingStates.waiting_for_data_confirmation)
    assert instance_five.survey_stage == 3
    assert instance_five.recipes == {'капучино': {'молоко': 67}}


@pytest.mark.asyncio
async def test_saving(instance_six,
                      mock_show_data,
                      mock_delete_kb,
                      mock_buttons_yes_not,
                      mock_check_correctness):
    result_yes = await main.saving('да', instance_six)
    result_else = await main.saving('some', instance_six)

    assert result_yes == (f'{t.SHOW_DATA}\n\n{constants.INPUT_START}',
                          t.DELETE_KB,
                          States.clear)
    assert result_else == (t.CHECKING_CORRECTNESS,
                           t.BUTTONS_YES_NOT,
                           FillingStates.waiting_for_data_confirmation)




