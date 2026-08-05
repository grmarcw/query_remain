from functools import wraps

import pytest

import core
from bot.context import InitialData as RecipesData
from core.check_data import init_user_data
from constants import constants_for_tests

@pytest.fixture
def instance_stage_one():
    instance = RecipesData()
    init_user_data(instance)
    instance.ingredients = ['молоко', 'зерно']
    instance.cifc = 'молоко'
    return instance


@pytest.fixture
def mock_render_list(mocker):
    mock = mocker.patch('core.renderers.render_list')
    mock.return_value = constants_for_tests.LIST_TEXT
    return mock


@pytest.fixture
def mock_buttons_yes_not(mocker):
    mock_button = mocker.patch('core.change_data.buttons_yes_or_not')
    mock_button.return_value = constants_for_tests.BUTTONS_YES_NOT
    return mock_button


@pytest.fixture
def mock_button_generator(mocker):
    mock = mocker.patch('core.change_data.button_generator')
    mock.return_value = constants_for_tests.BUTTON_GENERATOR
    return mock


@pytest.fixture
def mock_button_choose(mocker):
    mock = mocker.patch('core.change_data.buttons_choose_action')
    mock.return_value = constants_for_tests.BUTTON_CHOOSE
    return mock


@pytest.fixture
def mock_delete_kb(mocker):
    mock = mocker.patch('core.change_data.ReplyKeyboardRemove')
    mock.return_value = constants_for_tests.DELETE_KB
    return mock


@pytest.fixture
def mock_render_dict(mocker):
    mock = mocker.patch('core.renderers.render_dict')
    mock.return_value = constants_for_tests.RENDER_DICT
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
def mock_recipes(mocker):
    mock = mocker.patch('core.renderers.show_recipes')
    mock.format.return_value = constants_for_tests.RECIPES
    return mock


@pytest.fixture
def instance_stage_three():
    instance = RecipesData()
    init_user_data(instance)
    instance.survey_stage = 3
    instance.compositions = {'молоко': ['капучино']}
    instance.recipes = {'капучино': {'молоко': 6767}}
    instance.pfc = 'капучино'
    instance.cil = ['молоко']
    instance.cpl = ['капучино']
    return instance


@pytest.fixture
def mock_not_exist(mocker):
    mock = mocker.patch('core.change_data.answer.POSITION_DONT_EXIST')
    mock.format.return_value = constants_for_tests.DONT_EXIST
    return mock

@pytest.fixture
def mock_product_not_exist(mocker):
    mock = mocker.patch('core.change_data.answer.PRODUCT_DONT_EXIST')
    mock.format.return_value = constants_for_tests.DONT_EXIST
    return mock

@pytest.fixture
def mock_ask_pos_for_change(mocker):
    mock = mocker.patch('core.change_data.answer.ASK_POSITION_FOR_CHANGE',
                        new = constants_for_tests.ASK_PRODUCT)
    return mock


@pytest.fixture
def mock_success(mocker):
    mock = mocker.patch('core.change_data.answer.CHOOSE_POSITION_FOR_CHANGE')
    mock.format.return_value = constants_for_tests.SUCCESS
    return mock


@pytest.fixture
def mock_ask_quantity(mocker):
    mock = mocker.patch('core.change_data.answer.ASK_QUANTITY')
    mock.__str__ = mocker.MagicMock(return_value=constants_for_tests.QUANTITY)
    return mock

@pytest.fixture
def mock_ask_quantity_format(mocker):
    mock = mocker.patch('core.change_data.answer.ASK_QUANTITY')
    mock.format.return_value = constants_for_tests.QUANTITY
    return mock

@pytest.fixture
def mock_checking_constant(mocker):
    mock = mocker.patch('core.change_data.answer.CHECKING_CORRECT_DATA')
    mock.format.return_value = constants_for_tests.CHECKING_CORRECTNESS
    return mock

