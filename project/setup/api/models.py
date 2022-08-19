from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(),
    'name': fields.String(100),
})

director: Model = api.model('Режиссер', {
    'id': fields.Integer(),
    'name': fields.String(100),
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(),
    'title': fields.String(required=True, max_length=100),
    'description': fields.String(100),
    'trailer': fields.String(100),
    'year': fields.Integer(),
    'rating': fields.Float(),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director),
 })

user: Model = api.model('Пользователь', {
    'id': fields.Integer(),
    'email': fields.String(unique=True, nullable=False, max_length=100),
    'password': fields.String(nullable=False, max_length=255),
    'name': fields.String(100),
    'surname': fields.String(100),
    'favorite_genre': fields.Nested(genre),
})


