from flask_restful import Resource, reqparse, fields, marshal_with
from models import User, db


post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'username', dest='username',
    required=True,
    help='The user\'s username',
)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
}


class Register(Resource):
    def post(self):
        args = post_parser.parse_args()
        if User.query.filter_by(username=args['username']).count():
            return {'message': 'user already exist'}, 401
        user = User(username=args['username'])
        db.session.add(user)
        db.session.commit()
        return {'id': user.id, 'username': user.username}
