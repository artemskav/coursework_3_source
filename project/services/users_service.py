from typing import Optional

import jwt

from project.dao import UsersDAO

from project.exceptions import ItemNotFound
from project.models import User
from project.tools.security import generate_password_hash, generate_tokens, get_passw_from_token, user_token_by_email, \
    compare_password2


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
        return self.dao.create(email=email, password=passw)

    def get_user_by_email(self, email):
        """ Получение данных юзера по email """
        return self.dao.get_user_by_email(email)

    def check_user(self, email, password_on_test):
        """ Проверка пароля юзера   """
        user = self.get_user_by_email(email)
        return generate_tokens(email, user.password, password_on_test)

    def update_password(self, token, data_passwords):
        """ Обновление password """
        if compare_password2(token, data_passwords):
            email = user_token_by_email(token)
            return self.dao.update_password(email, data_passwords)
        return "Неправильный пароль или истекло время токена"

    def update_user(self, email, data_update):
        """ Внесение поправок в юзера   """
        return self.dao.update_user(email, data_update)
