from flask_socketio import Namespace, emit, send, join_room, leave_room


def emit_friends(user, message: str, obj: object) -> None:
    """Emit the specified message to each user's friend with the specified object"""

    print("gonna emit to all friends")
    for friend in user.friends:
        emit(message, obj, room=friend.username, namespace='/')


def emit_user(user, message: str, obj: object) -> None:
    """Emit the specified message to the specified user with the specified object"""

    emit(message, obj, room=user.username, namespace='/')
