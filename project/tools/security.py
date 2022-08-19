import base64
import hashlib
import hmac

from flask import current_app
import calendar
import datetime

import jwt
from flask_restx import abort


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def generate_tokens(email, password_hash, password, is_refresh=False):
    if email is None:
        raise abort(404)
    if not is_refresh:
        if not compare_password(password, password_hash):
            abort(401)
    data = {
        "email": email,
        "password": password
    }

    min15 = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
    data["exp"] = calendar.timegm(min15.timetuple())
    access_token = jwt.encode(data, key=current_app.config['SECRET_KEY'],
                              algorithm=current_app.config['ALGORITHM'])

    days130 = datetime.datetime.utcnow() + datetime.timedelta(
        days=current_app.config['TOKEN_EXPIRE_DAYS'])
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, key=current_app.config['SECRET_KEY'],
                               algorithm=current_app.config['ALGORITHM'])

    return {"access_token": access_token, "refresh_token": refresh_token}


def approve_refresh_token(refresh_token):
    data = jwt.decode(jwt=refresh_token, key=current_app.config['SECRET_KEY'],
                      algorithms=current_app.config['ALGORITHM'])
    username = data.get("username")

    return generate_tokens(username, None, is_refresh=True)


def compare_password(pwd_on_test, pwd_by_bd) -> bool:
    decoded_digest = base64.b64decode(pwd_on_test)

    hash_digest = hashlib.pbkdf2_hmac('sha256', pwd_by_bd.encode('utf-8'),
                                      current_app.config['PWD_HASH_SALT'],
                                      current_app.config['PWD_HASH_ITERATIONS'] )
    return hmac.compare_digest(decoded_digest, hash_digest)
