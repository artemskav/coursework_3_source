import jwt
from flask import request, abort, current_app


def auth_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)
        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(jwt=token, key=current_app.config['SECRET_KEY'],
                       algorithms=current_app.config['ALGORITHM'])
        except Exception as e:
            print("JWT Decode Exceptions", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper
