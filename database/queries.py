from sqlalchemy import select

from database.session import session_maker
from database.models import User


async def add_new_user(id: int, recipes: dict):
    """
    добавляем нового пользователя и данные о рецептах
    :param id: телеграмм-айди бота
    :param recipes: вложенный словарь с рецептами
    структура recipes: {товар:{ингридиент:кол-во ингр-та, идущего в этот товар}}
    :return: сохраняет в базу данных
    """
    async with session_maker() as sess:
        user = User(id=id, recipes=recipes)
        sess.add(user)
        await sess.commit()


async def get_user_data(id: int):
    """
    достает все данные пользователя из базы данных
    :param id: тг-айди пользователя для поиска его данных в бд
    :return: все данные кокретного пользователя
    """
    async with session_maker() as sess:
        user_data = await sess.execute(select(User).where(User.id == id))
        return user_data.scalar_one_or_none()


async def delete_user(id: int):
    """
    Удаляет данные пользователя из бд
    :param id: тг-айди пользователя
    """
    async with session_maker() as sess:
        user = await sess.get(User, id)
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
        new_data = User(id=id, deliveries=data)
        sess.add(new_data)
        await sess.commit()
