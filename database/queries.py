from sqlalchemy import select

from database.session import session_maker
from database.models import InitialData, SecondaryData


async def add_new_user(id: int, recipes: dict):
    """
    добавляем нового пользователя и данные о рецептах
    :param id: телеграмм-айди бота
    :param recipes: вложенный словарь с рецептами
    структура recipes: {товар:{ингридиент:кол-во ингр-та, идущего в этот товар}}
    :return: сохраняет в базу данных
    """
    async with session_maker() as sess:
        user = InitialData(id=id, recipes=recipes)
        sess.add(user)
        await sess.commit()


async def get_user_data(id: int, db_name=InitialData):
    """
    достает все данные пользователя из базы данных
    :param id: тг-айди пользователя для поиска его данных в бд
    :return: все данные кокретного пользователя
    """
    async with session_maker() as sess:
        user_data = await sess.execute(select(db_name).where(db_name.id == id))
        return user_data.scalar_one_or_none()


async def delete_user(id: int, name_db=InitialData):
    """
    Удаляет данные пользователя из бд
    :param id: тг-айди пользователя
    """
    async with session_maker() as sess:
        user = await sess.get(name_db, id)
        if user:
            await sess.delete(user)
            await sess.commit()


async def add_deliveries_info(id: int, data: dict):
    """
    добавляет данные о поставках в бд
    :param id: тг-айди юзера, которому нужно добавить инфу
    :param data: словарь с данными о поставках
    """
    async with session_maker() as sess:
        new_data = InitialData(id=id, deliveries=data)
        await sess.merge(new_data)
        await sess.commit()


async def delete_delivery(id: int):
    """
    Удаляет данные пользователя о поставках из бд
    :param id: тг-айди пользователя
    """
    async with session_maker() as sess:
        user = await sess.get(InitialData, id)
        if user:
            user.deliveries = None
            await sess.commit()

async def add_initial_balance(id:int, data: dict):
    '''
    Добавляет данные о стартовом остатке продукции
    '''
    async with session_maker() as sess:
        new_data = SecondaryData(id=id, initial_balance=data)
        sess.add(new_data)
        await sess.commit()
