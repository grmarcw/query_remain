import pytest

from bot.context import RecipesData
from constants import constants_for_tests
from core.check_data import init_user_data


@pytest.fixture
def instance_stage_one():
    instance = RecipesData()
    init_user_data(instance)
    instance.ingredients = ['молоко', 'зерно']
    instance.cifc = 'молоко'
    return instance

@pytest.fixture
def mock_button_generator(mocker):
    mock = mocker.patch('core.delete_data.button_generator')
    mock.return_value = constants_for_tests.BUTTON_GENERATOR
    return mock

@pytest.fixture
def mock_delete_kb(mocker):
    mock = mocker.patch('core.delete_data.ReplyKeyboardRemove')
    mock.return_value = constants_for_tests.DELETE_KB
    return mock

@pytest.fixture
def mock_button_show_delete(mocker):
    mock = mocker.patch('core.delete_data.buttons_show_delete')
    mock.return_value = constants_for_tests.BUTTONS_SHOW_DELETE
    return mock

@pytest.fixture
def mock_buttons_yes_not(mocker):
    mock_button = mocker.patch('core.delete_data.buttons_yes_or_not')
    mock_button.return_value = constants_for_tests.BUTTONS_YES_NOT
    return mock_button




@pytest.fixture
def mock_delete_data(mocker):
    mock = mocker.patch('core.delete_data.constants.INPUT_DATA_FOR_DELETE')
    mock.format.return_value = constants_for_tests.DELETE_DATA
    return mock






@pytest.fixture
def mock_render_recipes_str(mocker):
    mock = mocker.patch('core.renderers.show_recipes')
    mock.return_value=constants_for_tests.RECIPES
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






@pytest.fixture
def mock_exist_db_data(mocker):
    mock = mocker.patch('core.delete_data.queries.get_user_data')
    instance = RecipesData()
    instance.recipes == {'капучино': {'молоко': 250}}
    mock.return_value = instance
    return mock


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
def mock_deleted_position(mocker):
    mock = mocker.patch('core.renderers.constants.POSITION_IS_DELETED')
    mock.format.return_value=constants_for_tests.ELEMENT_DELETED
    return mock

@pytest.fixture
def mock_deleted_product(mocker):
    mock = mocker.patch('core.renderers.constants.PRODUCT_IS_DELETED')
    mock.format.return_value=constants_for_tests.ELEMENT_DELETED
    return mock

@pytest.fixture
def mock_position_not_exist(mocker):
    mock = mocker.patch('core.renderers.constants.PRODUCT_DONT_EXIST')
    mock.format.return_value=constants_for_tests.DONT_EXIST
    return mock















