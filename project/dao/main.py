from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.models import Genre, Movie, Director, User
from project.tools.security import generate_password_hash


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all(self, filter=None, page=None):
        stmt: BaseQuery = self._db_session.query(self.__model__)

        if filter == 'new':
            stmt = stmt.order_by(desc(self.__model__.year))
        else:
            stmt = stmt.order_by(self.__model__.year)

        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []

        return stmt.all()

class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def create(self, email, password):
        user = User(email=email, password=generate_password_hash(password))
        try:
            self._db_session.add(user)
            self._db_session.commit()
            print("++")
        except Exception as e:
            self._db_session.rollback()
            print(e)

    def get_user_by_email(self, email) -> User:
        user = self._db_session.query(self.__model__).filter(self.__model__.email == email).one()
        return user

    def update_user(self, email, data):
        """ Обновление данных по юзеру """
        user = self._db_session.query(self.__model__).filter(self.__model__.email == email).one()
        user.name = data.get('name')
        user.surname = data.get('surname')
        user.favorite_genre = data.get('favorite_genre')

        try:
            self._db_session.add(user)
            self._db_session.commit()
            print("++")
        except Exception as e:
            self._db_session.rollback()
            print(e)
            return [], 401
        return " ", 201

    def update_password(self, email, data_passwords):
        user = self._db_session.query(self.__model__).filter(self.__model__.email == email).one()
        user.password = generate_password_hash(data_passwords.get('password_2'))
        try:
            self._db_session.add(user)
            self._db_session.commit()
            print("++")
        except Exception as e:
            self._db_session.rollback()
            print(e)
            return [], 401
        return " ", 201

