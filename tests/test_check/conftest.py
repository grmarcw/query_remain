from unittest.mock import MagicMock

import pytest

from bot.context import RecipesData
from constants import constants, constants_for_tests
from core.check_data import init_user_data


@pytest.fixture
def mock_exist_db_data(mocker):
    mock = mocker.patch('core.check_data.queries.get_user_data')
    mock.return_value = {'id': 1234, 'recipes': {'капучино': {'молоко': 250}}, 'deliveries': {'metro': ['молоко']}}
    return mock

@pytest.fixture
def mock_not_exist_db_data(mocker):
    mock = mocker.patch('core.check_data.queries.get_user_data')
    mock.return_value = None

@pytest.fixture
def mock_exist_delivery_data(mocker):
    user_mock = MagicMock()
    user_mock.recipes = {'капучино': {'молоко': 250}}
    user_mock.deliveries = {'metro': ['молоко']}
    mock = mocker.patch('core.check_data.queries.get_user_data')
    mock.return_value = user_mock

@pytest.fixture
def instance_stage_one():
    instance = RecipesData()
    init_user_data(instance)
    instance.ingredients = ['молоко', 'зерно']
    instance.cifc = 'молоко'
    return instance

@pytest.fixture
def mock_ask_ingredient(mocker):
    mock = mocker.patch('core.check_data.constants.ASK_LIST_INGREDIENTS',
                        new=constants_for_tests.ASK_INGREDIENT)
    return mock

@pytest.fixture
def mock_delete_kb(mocker):
    mock = mocker.patch('core.check_data.ReplyKeyboardRemove')
    mock.return_value = constants_for_tests.DELETE_KB
    return mock

@pytest.fixture
def mock_buttons_show_delete(mocker):
    mock = mocker.patch('core.check_data.buttons_show_delete')
    mock.return_value = constants_for_tests.BUTTONS_SHOW_DELETE

@pytest.fixture
def mock_button_choose(mocker):
    mock = mocker.patch('core.check_data.buttons_choose_action')
    mock.return_value = constants_for_tests.BUTTON_CHOOSE
    return mock

@pytest.fixture
def mock_button_generator(mocker):
    mock = mocker.patch('core.check_data.button_generator')
    mock.return_value = constants_for_tests.BUTTON_GENERATOR
    return mock

@pytest.fixture
def mock_buttons_yes_not(mocker):
    mock_button = mocker.patch('core.check_data.buttons_yes_or_not')
    mock_button.return_value = constants_for_tests.BUTTONS_YES_NOT
    return mock_button

@pytest.fixture
def instance_stage_two():
    instance = RecipesData()
    init_user_data(instance)
    instance.survey_stage = 2
    instance.compositions = {'молоко': ['капучино'], 'зерно': ['американо']}
    instance.cifc = 'молоко'
    instance.pfc = 'капучино'
    return instance


@pytest.fixture
def instance_stage_three():
    instance = RecipesData()
    init_user_data(instance)
    instance.survey_stage = 3
    instance.compositions = {'молоко': ['капучино']}
    instance.recipes = {'капучино': {'молоко': 6767}}
    instance.pfc = 'капучино'
    return instance


@pytest.fixture
def mock_ask_position(mocker):
    mock = mocker.patch('core.check_data.constants.ASK_LIST_POSITIONS')
    mock.format.return_value = constants_for_tests.ASK_PRODUCT
    return mock

@pytest.fixture
def mock_ask_position_wpii(mocker):
    mock = mocker.patch('core.check_data.constants.ASK_LIST_POSITIONS_WITHOUT_PRD_IS_ING')
    mock.format.return_value = constants_for_tests.ASK_PRODUCT
    return mock

@pytest.fixture
def mock_choose_position(mocker):
    mock = mocker.patch('core.check_data.constants.CHOOSE_POSITION_FOR_CHANGE')
    mock.format.return_value = constants_for_tests.CHOOSE_POSITION
    return mock

@pytest.fixture
def mock_choose_position_str(mocker):
    mock = mocker.patch('core.check_data.constants.CHOOSE_POSITION_FOR_CHANGE')
    mock.__str__ = mocker.MagicMock(return_value = constants_for_tests.CHOOSE_POSITION)
    return mock

@pytest.fixture
def mock_ask_quantity(mocker):
    mock = mocker.patch('core.check_data.constants.ASK_QUANTITY')
    mock.format.return_value = constants_for_tests.QUANTITY
    return mock

@pytest.fixture
def mock_render_list(mocker):
    mock = mocker.patch('core.renderers.render_list')
    mock.return_value = constants_for_tests.LIST_TEXT
    return mock

@pytest.fixture
def mock_render_dict(mocker):
    mock = mocker.patch('core.renderers.render_dict')
    mock.return_value = constants_for_tests.RENDER_DICT
    return mock


