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


class PendingFriend(Resource):
    # Protecred endpoint
    method_decorators = [authenticate]

    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(
            'id', dest='id',
            required=True,
            help='Required field id',
        )

    # Get all pending friend requests
    def get(self, user):
        return marshal(user.pending_friends, user_fields)

    # Validate a pending friend request
    def post(self, user):
        args = self.post_parser.parse_args()
        try:
            id = int(args['id'])
        except:
            return {'message': 'id must be a number'}
        pending_friend = None
        for i in user.pending_friends:
            if i.id == id:
                pending_friend = i
        if pending_friend is None:
            return {'message': 'pending friend not found'}, 401
        # Remove pending friend request
        user.pending_friends.remove(pending_friend)

        # Add friends
        user.friends.append(pending_friend)
        pending_friend.friends.append(user)

        # Commit changes
        db.session.add(user)
        db.session.add(pending_friend)
        db.session.commit()
        return {}
