from flask_socketio import Namespace, emit, send, join_room, leave_room


def emit_friend(user, message: str, obj: object) -> None:
    """Emit the specified message to each user's friend with the specified Object"""

    for friend in user.friends:
        emit(message, obj, room=friend.username, namespace='/')
