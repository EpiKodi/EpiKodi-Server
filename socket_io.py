from flask_socketio import Namespace, emit, send, join_room, leave_room
import sys
from common.auth import get_user
import common.ws as ws


class Socket(Namespace):
    def on_join(self, data):
        print("JOINED !", file=sys.stderr)
        print(data.get('token'), file=sys.stderr)
        if data.get('token') is None:
            return
        try:
            user = get_user(data['token'])
        except:
            return
        print(user.username, file=sys.stderr)
        print("JOIN SUCCESS")
        join_room(user.username)

    def on_left(self, data):
        if data.get('token') is None:
            return
        try:
            user = get_user(data['token'])
        except:
            return
        leave_room(user.username)

    def on_media_update(self, data):
        if data.get('token') is None:
            return
        try:
            user = get_user(data['token'])
        except:
            return
        ws.emit_friends(user, 'media_update',
                        {
                            'timer': data.get('timer'),
                            'play': data.get('play'),
                            'id': data.get('id')
                        })
