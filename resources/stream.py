import sys
from flask import request, send_file
from flask_restful import Resource, reqparse, fields, marshal
from common.auth import authenticate
from models import db
import common.ws as ws

class Stream(Resource):
    # Protected endpoint for delete method
    method_decorators = [authenticate]

    # List all the files that friends are streaming
    def get(self, user):
        ws.emit_friend(user, "stream", {"user": user.username})
        return {}

    # Start a stream
    def post(self, user):
        pass

    # End a stream
    def delete(self, user):
        pass
