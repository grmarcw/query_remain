import pytest

from bot.context import InitialData as RecipesData
from constants import constants_for_tests
from core.check_data import init_user_data

@pytest.fixture
def instance_zero():
    instance = RecipesData()
    init_user_data(instance)
    instance.ingredients = ['боул']

    return instance

@pytest.fixture
def instance_one():
    instance = RecipesData()
    init_user_data(instance)
    instance.ingredients = ['молоко', 'зерно', 'боул']

    return instance

@pytest.fixture
def instance_two():
    instance = RecipesData()
    init_user_data(instance)
    instance.ingredients = ['молоко']

    return instance

@pytest.fixture
def instance_three():
    instance = RecipesData()
    init_user_data(instance)
    instance.cil = ['молоко']
    instance.cpl = ['капучино', 'латте']
    instance.recipes = {'капучино': {'молоко': 0}, 'латте': {'зерно':0}}

    return instance

@pytest.fixture
def instance_four():
    instance = RecipesData()
    init_user_data(instance)
    instance.cil = ['молоко', 'зерно']
    instance.cpl = ['капучино']
    instance.recipes = {'капучино': {'молоко': 0, 'зерно': 0}}

    return instance

@pytest.fixture
def instance_five():
    instance = RecipesData()
    init_user_data(instance)
    instance.cil = ['молоко']
    instance.cpl = ['капучино']
    instance.recipes = {'капучино': {'молоко': 0}}

    return instance

@pytest.fixture
def instance_six():
    instance = RecipesData()
    init_user_data(instance)
    instance.ingredients_without_products = ['боул']
    instance.recipes = {'капучино': {'молоко': 0}}

    return instance



@pytest.fixture
def mock_ask_positions(mocker):
    mock = mocker.patch('core.main.constants.ASK_LIST_POSITIONS')
    mock.format.return_value = constants_for_tests.ASK_PRODUCT



@pytest.fixture
def mock_delete_kb(mocker):
    mock = mocker.patch('core.main.ReplyKeyboardRemove')
    mock.return_value = constants_for_tests.DELETE_KB
    return mock

@pytest.fixture
def mock_buttons_yes_not(mocker):
    mock_button = mocker.patch('core.main.buttons_yes_or_not')
    mock_button.return_value = constants_for_tests.BUTTONS_YES_NOT
    return mock_button

@pytest.fixture
def mock_delete_kb(mocker):
    mock = mocker.patch('core.main.ReplyKeyboardRemove')
    mock.return_value = constants_for_tests.DELETE_KB
    return mock



@pytest.fixture
def mock_render_dict(mocker):
    mock = mocker.patch('core.renderers.render_dict')
    mock.return_value = constants_for_tests.RENDER_DICT
    return mock

@pytest.fixture
def mock_ask_quantity(mocker):
    mock = mocker.patch('core.main.constants.ASK_QUANTITY')
    mock.format.return_value = constants_for_tests.QUANTITY
    return mock

@pytest.fixture
def mock_check_correctness(mocker):
    mock = mocker.patch('core.main.constants.CHECKING_CORRECT_DATA')
    mock.format.return_value = constants_for_tests.CHECKING_CORRECTNESS
    return mock


@pytest.fixture
def mock_db(mocker):
    mock = mocker.patch('core.main.queries.add_new_user')
    mock.format.return_value = ''
    return mock


@pytest.fixture
def mock_show_data(mocker):
    mock = mocker.patch('core.main.constants.SHOW_SAVING_DATA')
    mock.format.return_value = constants_for_tests.SHOW_DATA
    return mock
