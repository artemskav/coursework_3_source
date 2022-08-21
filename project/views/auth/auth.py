from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user
from project.tools.decorators import auth_required
from project.tools.security import approve_refresh_token

api = Namespace('auth')


@api.route('/register/')
class RegisterView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def post(self):
        """        Create of user.        """
        data = request.json
        if data.get('email') and data.get('password'):
            return user_service.create(data.get('email'), data.get('password')), 201
        return "no Ok", 401


@api.route('/login/')
class LoginView(Resource):
    @api.response(404, 'Not Found')
#    @auth_required
#    @api.marshal_with(user, code=200, description='OK')
    def post(self):
        """        Login of user.        """

        data = request.json
        if data.get('email') and data.get('password'):
            return user_service.check_user(data.get('email'), data.get('password')), 201
        return "no Ok", 401

    @auth_required
    def put(self):
        """        Update token        """
        data = request.json
        if data.get("access_token") and data.get("refresh_token"):
            return approve_refresh_token(data.get("refresh_token")), 201
        return "no Ok", 401
