import sys
from flask import request, send_file
from flask_restful import Resource, reqparse, fields, marshal
from common.auth import authenticate
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
    method_decorators = [authenticate]

    # List all the files that friends are streaming
    def get(self, user):
        all_stream = []
        for friend in user.friends:
            if friend.stream is not None:
                all_stream += friend.stream
        return marshal(all_stream, file_fields)

    # Start a stream
    def post(self, user):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument(
            'id', dest='id',
            required=True,
            help='Required field id',
        )
        args = post_parser.parse_args()
        args['id']
        # WebSocket call
        ws.emit_friend(user, "stream", {"user": user.username})
        return {}

    # End a stream
    def delete(self, user):
        pass
