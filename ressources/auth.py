from flask_restful import Resource, reqparse, fields, marshal
from models import User, db

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
}


class Register(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            'username', dest='username',
            required=True,
            help='Required field username',
        )

    def post(self):
        args = self.post_parser.parse_args()
        if User.query.filter_by(username=args['username']).count():
            return {'message': 'user already exist'}, 401
        user = User(username=args['username'])
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
        return {}
