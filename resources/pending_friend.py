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


class PendingFriend(Resource):
    # Protecred endpoint
    method_decorators = [authenticate, prevent_missing_id]

    # Get all pending friend requests
    def get(self, user, **kwargs):
        return marshal(user.pending_friends, user_fields)

    # Validate a pending friend request
    def post(self, id, user):
        if id is None:
            return {'error': 'missing slug parameter'}, 400
        pending_friend = None
        for i in user.pending_friends:
            if i.id == id:
                pending_friend = i
        if pending_friend is None:
            return {'error': 'pending friend not found'}, 400
        # Remove pending friend request
        user.pending_friends.remove(pending_friend)

        # Add friends
        user.friends.append(pending_friend)
        pending_friend.friends.append(user)

        # Commit changes
        db.session.add(user)
        db.session.add(pending_friend)
        db.session.commit()

        # WebSocket call
        ws.emit_user(pending_friend, 'friend-accepted', {'user': user.username})
        return {}

    # Refuse a pending friend request
    def delete(self, id, user):
        if id is None:
            return {'error': 'missing slug parameter'}, 400
        pending_friend = None
        for i in user.pending_friends:
            if i.id == id:
                pending_friend = i
        if pending_friend is None:
            return {'error': 'pending friend not found'}, 400
        # Remove pending friend request
        user.pending_friends.remove(pending_friend)

        # Commit changes
        db.session.add(user)
        db.session.commit()
        return {}
