from flask_restful import Resource, reqparse, fields, marshal
from common.auth import authenticate
from common.misc import prevent_missing_id
from models import User as U
from models import db
from numbers import Number
import sys
import common.ws as ws

user_fields = {
    'id': fields.String,
    'username': fields.String
}


class Friend(Resource):
    # Protecred endpoint
    method_decorators = [authenticate, prevent_missing_id]

    # Get all friends
    def get(self, user, **kwargs):
        return marshal(user.friends, user_fields)

    # Create a pending friend request
    def post(self, id, user):
        if id is None:
            return {'message': 'missing slug parameter'}
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

        # WebSocket call
        ws.emit_user(friend, 'friend-request', {'user': user.username})
        return {}

    # Remove a friend
    def delete(self, id, user):
        if id is None:
            return {'message': 'missing slug parameter'}
        friend = None
        for i in user.friends:
            if i.id == id:
                friend = i
        if friend is None:
            return {'message': 'friend not found'}, 401
        # Remove friend
        user.friends.remove(friend)
        friend.friends.remove(user)

        # Commit changes
        db.session.add(user)
        db.session.add(friend)
        db.session.commit()
        return {}
