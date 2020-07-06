from flask_restful import Resource, reqparse, fields, marshal
from common.auth import authenticate
from models import User as U
from models import db
from numbers import Number
import sys

user_fields = {
    'id': fields.Integer,
    'username': fields.String
}


class Friend(Resource):
    # Protecred endpoint
    method_decorators = [authenticate]

    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            'id', dest='id',
            required=True,
            help='Required field id',
        )

    # Get all friends
    def get(self, user):
        return marshal(user.friends, user_fields)

    # Create a pending friend request
    def post(self, user):
        args = self.post_parser.parse_args()
        try:
            id = int(args['id'])
        except:
            return {'message': 'id must be a number'}
        friend = U.query.filter_by(id=id).first()
        if friend is None:
            return {'message': 'user not found'}, 401
        if friend is user:
            return {'message': 'you cannot self-add'}, 401
        if friend in user.friends:
            return {'message': 'you are already friend'}, 401
        # Add pending friend request
        friend.pending_friends.append(user)

        # Commit changes
        db.session.add(friend)
        db.session.commit()
        return {}
