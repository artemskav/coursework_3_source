from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    __tablename__ = 'directors'

    name = Column(String(100), unique=True, nullable=False)


class Movie(models.Base):
    __tablename__ = 'movies'

    title = Column(String(100))
    description = Column(String(100))
    trailer = Column(String(100))
    year = Column(Integer)
    rating = Column(Float)
    genre_id = Column(Integer, ForeignKey(f"{Genre.__tablename__}.id"))
    director_id = Column(Integer, ForeignKey(f"{Director.__tablename__}.id"))
    genre = relationship("Genre")
    director = relationship("Director")


class User(models.Base):
    __tablename__ = 'users'

    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(100))
    surname = Column(String(100))
    favorite_genre = Column(Integer, ForeignKey(f"{Genre.__tablename__}.id"))
