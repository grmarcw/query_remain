import pytest
from sqlalchemy.ext.asyncio import result

from bot.states_fsm import DeleteStates, FillingStates
from constants import constants_for_tests as t, constants

from core import delete_data


@pytest.mark.asyncio
async def test_handle_show_or_delete_request(instance_stage_one,
                                             mock_delete_data,
                                             mock_button_generator,
                                             mock_render_recipes_str,
                                             mock_delete_kb,
                                             mock_button_show_delete,
                                             mock_exist_db_data):
    result_for_delete = await delete_data.handle_show_or_delete_request(
        'удалить', instance_stage_one
    )
    result_for_show = await delete_data.handle_show_or_delete_request(
        'отобразить', instance_stage_one
    )
    result_else = await delete_data.handle_show_or_delete_request(
        'что-то', instance_stage_one
    )
    assert result_for_delete == (t.DELETE_DATA,
                                 t.BUTTON_GENERATOR,
                                 DeleteStates.waiting_for_deletion_data_type)
    assert result_for_show == (f'{t.RECIPES}\n{constants.INPUT_START}',
                               t.DELETE_KB,
                               None)
    assert result_else == (constants.SHOW_OR_DELETE,
                           t.BUTTONS_SHOW_DELETE,
                           None)


def test_delete_element(instance_stage_one,
                        instance_stage_two,
                        mock_render_list,
                        mock_render_dict,
                        mock_buttons_yes_not,
                        mock_button_generator,
                        mock_deleted_product,
                        mock_deleted_position,
                        mock_position_not_exist):
    result_cancel_stage_one = delete_data.delete_element(
        'отменить', instance_stage_one
    )
    result_cancel_stage_two = delete_data.delete_element(
        'отменить', instance_stage_two
    )
    result_stage_one = delete_data.delete_element(
        'молоко', instance_stage_one
    )
    result_stage_two = delete_data.delete_element(
        'капучино', instance_stage_two
    )
    result_else = delete_data.delete_element(
        'что-то', instance_stage_one
    )

    assert result_cancel_stage_one == (t.LIST_TEXT,
                                       t.BUTTONS_YES_NOT,
                                       FillingStates.waiting_for_data_confirmation)
    assert result_cancel_stage_two == (t.RENDER_DICT,
                                       t.BUTTONS_YES_NOT,
                                       FillingStates.waiting_for_data_confirmation)
    assert result_stage_one == (f'{t.ELEMENT_DELETED}\n{t.LIST_TEXT}',
                                t.BUTTONS_YES_NOT,
                                FillingStates.waiting_for_data_confirmation)
    assert result_stage_two == (f'{t.ELEMENT_DELETED}\n{t.RENDER_DICT}',
                                t.BUTTONS_YES_NOT,
                                FillingStates.waiting_for_data_confirmation)
    assert result_else == (t.DONT_EXIST,
                           t.BUTTON_GENERATOR,
                           None)

