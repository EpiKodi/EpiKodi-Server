import sys
from flask import request, send_file
from flask_restful import Resource, reqparse, fields, marshal
from common.auth import authenticate
from common.misc import prevent_missing_id
from models import User as U
from models import File as F
from models import db
import common.ws as ws

file_fields = {
    'id': fields.String,
    'filename': fields.String,
    'user': fields.String,
    'extension': fields.String
}


class Stream(Resource):
    # Protected endpoint for delete method
    method_decorators = [authenticate, prevent_missing_id]

    # List all the files that friends are streaming
    def get(self, user, **kwargs):
        all_stream = []
        for friend in user.friends:
            if friend.stream is not None:
                all_stream.append(friend.stream)
        return marshal(all_stream, file_fields)

    # Start a stream
    def post(self, id, user):
        if user.stream is not None:
            return {'error': 'You are already streaming'}, 400
        file = F.query.filter_by(id=id).first()
        if file is None:
            return {'error': 'File not found'}, 400

        # Add stream
        user.stream = file

        # Commit changes
        db.session.add(user)
        db.session.commit()

        # WebSocket call
        ws.emit_friends(user, "stream", {"user": user.username})
        return {}

    # End a stream
    def delete(self, user, **kwargs):
        if user.stream is None:
            return {'error': 'You are not streaming'}, 400

        # Remove stream
        user.stream = None

        # Commit changes
        db.session.add(user)
        db.session.commit()

        # WebSocket call
        ws.emit_friends(user, "end-stream", {"user": user.username})
        return {}
