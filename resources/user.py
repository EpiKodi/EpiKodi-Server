from flask_restful import Resource, reqparse, fields, marshal
from common.auth import authenticate
from models import User as U

import sys

user_fields = {
    'id': fields.Integer,
    'username': fields.String
}

class User(Resource):
    # Protecred endpoint
    method_decorators = [authenticate]

    # Search user from 'username'
    def get(self, username, user):
        users = U.query.filter(U.username.like('%' + username + '%')).all()
        return marshal(users, user_fields)