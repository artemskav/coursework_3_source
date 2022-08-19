from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.parsers import page_parser

from project.setup.api.models import user

api = Namespace('user')

@api.route('/')
class RegisterView(Resource):
    @api.expect(page_parser)
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def get(self):
        """        Get all users.        """
        return user_service.get_all(**page_parser.parse_args())


    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def patch(self):
        """        Change data of user.        """

        data = request.json
        user.name = data.get('name')
        user.surname = data.get('surname')
        user.favorite_genre = data.get('favorite_genre')
        return user_service.update(user), 201

@api.route('/login')
class LoginView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    def post(self):
        """        Login of user.        """

        data = request.json
        if email := data.get('email'):
            if password := data.get('password'):
                return user_service.check(email, password), 201
        return "no Ok", 401

    def put(self):
        """        Login of user.        """

        data = request.json
        if access_token := data.get('access_token'):
            if refresh_token := data.get('refresh_token'):
                return user_service.update_token(access_token, refresh_token), 201
        return "no Ok", 401

