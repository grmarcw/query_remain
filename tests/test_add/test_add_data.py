import pytest

from bot.states_fsm import FillingStates
from core.add_data import add_data_in_instance


def test_add_data(instance_stage_one,
                  instance_stage_two,
                  mock_render_list,
                  mock_buttons_yes_not,
                  mock_render_dict,
                  ):

    result_stage_one = add_data_in_instance('моЛоко  ,Зерно  ', instance_stage_one)
    result_stage_two = add_data_in_instance('капучино, Латте', instance_stage_two)

    assert result_stage_one == ('список', 'кнопки да/нет', FillingStates.waiting_for_data_confirmation)
    assert instance_stage_one.ingredients == ['молоко', 'зерно']
    assert result_stage_two == ('словарь', 'кнопки да/нет', FillingStates.waiting_for_data_confirmation)
    assert instance_stage_two.compositions == {'молоко': ['капучино', 'латте']}

