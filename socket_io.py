from flask_socketio import Namespace, emit, send, join_room, leave_room
import sys


class Socket(Namespace):
    def on_join(self, data):
        print(data, file=sys.stderr)
        if data.get('room') is None:
            return
        join_room(data['room'])
        emit('new_user', room=data['room'])

    def on_message(self, data):
        emit('message', data, room=data['room'])

    def on_left(self, data):
        leave_room(data['room'])