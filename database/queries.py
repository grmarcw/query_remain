from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from session import session_maker
from models import InitialData, SecondaryData


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


async def add_new_info(id: int, column, data: dict):
    """
    добавляет данные о поставках в бд
    :param id: тг-айди юзера, которому нужно добавить инфу
    :param data: словарь с данными о поставках
    """
    async with session_maker() as sess:
        if column == "deliveries":
            new_data = InitialData(id=id, deliveries=data)
        elif column == "positions_products":
            new_data = InitialData(id=id, positions_products=data)
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


async def add_initial_balance(id: int, data: dict):
    """
    Добавляет данные о стартовом остатке продукции
    """
    async with session_maker() as sess:
        new_data = SecondaryData(id=id, initial_balance=data)
        sess.add(new_data)
        await sess.commit()

async def add_daily_data(id: int, daily_data: dict):
    async with session_maker() as sess:
        user = await sess.get(SecondaryData, id)
        user.data = user.data + [daily_data]
        await sess.commit()


async def delete_daily_data(id, date):
    async with session_maker() as sess:
        user = await sess.get(SecondaryData, id)
        index_dict_for_delete = None
        for index, data_dict in enumerate(user.data):
            if date in data_dict:
                index_dict_for_delete = index
                break

        del user.data[index_dict_for_delete]
        flag_modified(user, 'data')
        await sess.commit()





