from flask import request
from functools import wraps
from flask_restful import abort
from models import User
import jwt
import os

import sys


def authenticate(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if request.headers.get('Authorization') is None:
            abort(401)
        token = request.headers['Authorization'].split(',')[0]
        try:
            jwt_token = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
        except:
            abort(401)
        user = User.query.filter_by(id=jwt_token['id']).first()
        if user is None:
            abort(401)
        kwargs['user'] = user
        return function(**kwargs)
    return wrapper


def get_user(token: str):
    try:
        jwt_token = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
    except:
        abort(401)
    user = User.query.filter_by(id=jwt_token['id']).first()
    if user is None:
        abort(401)
    return user
