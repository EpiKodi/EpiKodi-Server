from flask_socketio import Namespace, emit, send, join_room, leave_room
import sys
from common.auth import get_user


class Socket(Namespace):
    def on_join(self, data):
        if data.get('token') is None:
            return
        try:
            user = get_user(data['token'])
        except:
            return
        join_room(user.username)

    def on_left(self, data):
        if data.get('token') is None:
            return
        try:
            user = get_user(data['token'])
        except:
            return
        leave_room(user.username)
