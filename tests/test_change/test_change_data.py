

from bot.states_fsm import FillingStates, ChangingData
from core import change_data
from constants import constants_for_tests as t
from constants import constants


def test_get_element_for_change_stage_one(
        instance_stage_one,
        mock_render_list,
        mock_buttons_yes_not,
        mock_button_generator,
        mock_delete_kb,
        mock_not_exist
):

    result_for_cancel = change_data.get_element_for_change('отменить', instance_stage_one)
    result_for_diff_element = change_data.get_element_for_change('элемент не из списка', instance_stage_one)
    result = change_data.get_element_for_change('молоко', instance_stage_one)

    assert result_for_cancel == (t.LIST_TEXT,
                                 t.BUTTONS_YES_NOT,
                                 FillingStates.waiting_for_data_confirmation)
    assert result_for_diff_element == (t.DONT_EXIST,
                                       t.BUTTON_GENERATOR,
                                       None)
    assert result == ("Введите новое название для позиции",
                      t.DELETE_KB,
                      ChangingData.change)

def test_get_element_for_change_stage_two(
        instance_stage_two,
        mock_render_dict,
        mock_buttons_yes_not,
        mock_delete_kb

):
    result_for_cancel = change_data.get_element_for_change('отменить', instance_stage_two)
    assert result_for_cancel == ('словарь',
                                 t.BUTTONS_YES_NOT,
                                 FillingStates.waiting_for_data_confirmation)


def test_change_data_stage_one(instance_stage_one,
                               mock_render_list,
                               mock_buttons_yes_not
                               ):
    result_for_cancel = change_data.change_data('отменить', instance_stage_one)
    result = change_data.change_data('сливки', instance_stage_one)

    assert result_for_cancel == (t.LIST_TEXT,
                                 t.BUTTONS_YES_NOT,
                                 FillingStates.waiting_for_data_confirmation)
    assert result == (t.LIST_TEXT,
                      t.BUTTONS_YES_NOT,
                      FillingStates.waiting_for_data_confirmation)
    assert instance_stage_one.ingredients == ['сливки','зерно']

def test_change_data_stage_two(instance_stage_two,
                               mock_render_dict,
                               mock_buttons_yes_not
                               ):
    result_for_cancel = change_data.change_data('отменить', instance_stage_two)
    result = change_data.change_data('капуч', instance_stage_two)

    assert result_for_cancel == (t.RENDER_DICT,
                                 t.BUTTONS_YES_NOT,
                                 FillingStates.waiting_for_data_confirmation)
    assert result == (t.RENDER_DICT,
                      t.BUTTONS_YES_NOT,
                      FillingStates.waiting_for_data_confirmation)
    assert instance_stage_two.compositions == {'молоко': ['капуч'], 'зерно': ['американо']}


def test_get_composition_for_change_stage_two(instance_stage_two,
                                              mock_render_dict,
                                              mock_not_exist,
                                              mock_buttons_yes_not,
                                              mock_success,
                                              mock_button_choose):
    result_for_cancel = change_data.get_composition_for_change(
        "отменить", instance_stage_two
    )
    result_for_incorrect_position = change_data.get_composition_for_change(
        "сливки", instance_stage_two
    )
    result = result_for_incorrect_position = change_data.get_composition_for_change(
        "молоко", instance_stage_two
    )
    assert result_for_cancel == (t.RENDER_DICT,
                                 t.BUTTONS_YES_NOT,
                                 FillingStates.waiting_for_data_confirmation)
    assert result_for_incorrect_position == (t.DONT_EXIST, t.BUTTON_GENERATOR, None)
    assert result == (t.SUCCESS,
                      t.BUTTON_CHOOSE,
                      ChangingData.waiting_result_choosing_action)


def test_get_composition_for_change_stage_three(instance_stage_three,
                                              mock_render_dict,
                                              mock_ask_quantity,
                                              mock_not_exist,
                                              mock_buttons_yes_not,
                                              mock_success,
                                              mock_button_choose):
    result_for_cancel = change_data.get_composition_for_change(
        "отменить", instance_stage_three
    )
    result_for_incorrect_position = change_data.get_composition_for_change(
        "сливки", instance_stage_three
    )
    result = result_for_incorrect_position = change_data.get_composition_for_change(
        "молоко", instance_stage_three)

    assert result_for_cancel == (t.RENDER_DICT,
                                 t.BUTTONS_YES_NOT,
                                 FillingStates.waiting_for_data_confirmation)
    assert result_for_incorrect_position == (t.DONT_EXIST,
                                             t.BUTTON_CHOOSE, None)
    assert result == (t.QUANTITY,
                      t.DELETE_KB,
                      ChangingData.waiting_new_quantity)

def test_recomposites(instance_stage_three,
                      mock_render_dict,
                      mock_buttons_yes_not,
                      mock_ask_quantity,
                      mock_delete_kb):
    result_incorrect = change_data.recomposites('один', instance_stage_three)
    result = change_data.recomposites(67, instance_stage_three)

    assert result_incorrect == (
    f'{constants.INCORRECT_INPUT}\n{t.QUANTITY}',
        t.DELETE_KB,
        None
    )
    assert result == (
        t.RENDER_DICT,
        t.BUTTONS_YES_NOT,
        FillingStates.waiting_for_data_confirmation
    )

def test_get_position_name_for_change(instance_stage_three,
                                      mock_checking_constant,
                                      mock_buttons_yes_not,
                                      mock_product_not_exist,
                                      mock_button_generator):
    result_for_cancel = change_data.get_position_name_for_change(
        'отменить',
        instance_stage_three)
    result_for_diff_element = change_data.get_position_name_for_change(
        'элемент не из словаря',
        instance_stage_three)
    result = change_data.get_position_name_for_change(
        'капучино',
        instance_stage_three
    )

    assert result_for_cancel == (t.CHECKING_CORRECTNESS,
                                 t.BUTTONS_YES_NOT,
                                 FillingStates.waiting_for_data_confirmation)
    assert result_for_diff_element == (t.DONT_EXIST,
                                       t.BUTTON_GENERATOR,
                                       None)
    assert result == (constants.ASK_PRODUCT_FOR_CHANGE,
                      t.BUTTON_GENERATOR,
                      ChangingData.waiting_ingredient_name)

def test_change_quantity(instance_stage_three,
                         mock_ask_quantity_format,
                         mock_delete_kb,
                         mock_buttons_yes_not,
                         mock_checking_constant):
    result_incorrect = change_data.change_quantity('один', instance_stage_three)
    result = change_data.change_quantity(1, instance_stage_three)

    assert result_incorrect == (f'{constants.INCORRECT_INPUT}\n{t.QUANTITY}',
                                t.DELETE_KB,
                                None)
    assert result == (t.CHECKING_CORRECTNESS,
                      t.BUTTONS_YES_NOT,
                      FillingStates.waiting_for_data_confirmation

                      )
