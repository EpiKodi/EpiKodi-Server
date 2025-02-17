from flask_restful import Resource, reqparse, fields, marshal
from models import User, db
from common.crypto import encode, decode
import jwt
import os
import uuid

user_fields = {
    'id': fields.String,
    'username': fields.String
}


class Register(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            'username', dest='username',
            required=True,
            help='Required field username',
        )

        self.post_parser.add_argument(
            'password', dest='password',
            required=True,
            help='Required field password'
        )

    def post(self):
        args = self.post_parser.parse_args()
        if User.query.filter_by(username=args['username']).count():
            return {'message': 'user already exist'}, 400
        user = User(id=uuid.uuid4().hex, username=args['username'], password=encode(args['password']))
        # need to prevent commit user with a '-' in his username
        db.session.add(user)
        db.session.commit()
        return marshal(user, user_fields)


class Login(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            'username', dest='username',
            required=True,
            help='Required field username',
        )

        self.post_parser.add_argument(
            'password', dest='password',
            required=True,
            help='Required field password'
        )

    def post(self):
        args = self.post_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user is None:
            return {'message': 'wrong username / password combinaison'}, 400
        if decode(user.password) != args['password']:
            return {'message': 'wrong username / password combinaison'}, 400
        encoded = jwt.encode({'id': user.id}, os.environ['JWT_SECRET'], algorithm='HS256')
        return {'token': encoded.decode('utf-8')}
