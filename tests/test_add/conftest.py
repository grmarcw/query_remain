import pytest
from pytest_mock import mocker

from bot.context import InitialData as RecipesData
from core.check_data import init_user_data


@pytest.fixture
def instance_stage_one():
    instance_for_test = RecipesData()
    init_user_data(instance_for_test)
    instance_for_test.survey_stage = 1
    instance_for_test.ingredients = []
    return instance_for_test

@pytest.fixture
def mock_render_list(mocker):
    mock_render = mocker.patch('core.renderers.render_list')
    mock_render.return_value = 'список'
    return mock_render

@pytest.fixture
def mock_buttons_yes_not(mocker):
    mock_button = mocker.patch('core.add_data.buttons_yes_or_not')
    mock_button.return_value = 'кнопки да/нет'
    return mock_button

@pytest.fixture
def instance_stage_two():
    instance_for_test = RecipesData()
    init_user_data(instance_for_test)
    instance_for_test.survey_stage = 2
    instance_for_test.compositions = {'молоко': []}
    instance_for_test.cifc = 'молоко'
    return instance_for_test

@pytest.fixture
def mock_render_dict(mocker):
    mock = mocker.patch('core.renderers.render_dict')
    mock.return_value = 'словарь'
    return mock