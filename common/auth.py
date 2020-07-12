from flask import request, jsonify, make_response
from functools import wraps
from flask_restful import abort
from models import User
import jwt
import os

import sys

AUTH_ERROR_MESSAGE = "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required."


def authenticate(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if request.headers.get('Authorization') is None:
            abort(make_response(jsonify(error=AUTH_ERROR_MESSAGE), 401))
        token = request.headers['Authorization'].split(',')[0]
        try:
            jwt_token = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
        except:
            abort(make_response(jsonify(error=AUTH_ERROR_MESSAGE), 401))
        user = User.query.filter_by(id=str(jwt_token['id'])).first()
        if user is None:
            abort(make_response(jsonify(error=AUTH_ERROR_MESSAGE), 401))
        kwargs['user'] = user
        return function(**kwargs)
    return wrapper


def get_user(token: str):
    try:
        jwt_token = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
    except:
        abort(make_response(jsonify(error=AUTH_ERROR_MESSAGE), 401))
    user = User.query.filter_by(id=jwt_token['id']).first()
    if user is None:
        abort(make_response(jsonify(error=AUTH_ERROR_MESSAGE), 401))
    return user
