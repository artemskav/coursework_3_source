from typing import Optional

from project.dao import UsersDAO
from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.tools.security import generate_password_hash, generate_tokens


class UsersService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def create(self, email, passw):
        """ Внесение в список нового юзера """
        return self.dao.create(email, passw)

    def get_user_by_email(self, email):
        """ Получение данных юзера по email """
        return self.dao.get_user_by_email(email)

    def check_user(self, email, password_on_test):
        user = self.get_user_by_email(email)
        return generate_tokens(email, user.password, password_on_test)

    # def put(self, uid):
    #     """ Удаление юзера из списка по id """
    #     user = self.dao.query(User).filter(User.id == uid).first()
    #     if not user:
    #         return "", 404
    #     self.session.delete(user)
    #     self.session.commit()
