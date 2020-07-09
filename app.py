import os
from cryptography.fernet import Fernet
from socket_io import Socket
from models import db
from resources.pending_friend import PendingFriend
from resources.friend import Friend
from resources.user import User
from resources.files import File, List
from resources.auth import Register, Login
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_restful import Resource, Api
from flask import Flask, Blueprint

# Flask config
app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = os.environ.get('DEBUG')
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__)) + '/files'

# SocketIO config
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
socketio = SocketIO(app, cors_allowed_origins="*")
socketio.on_namespace(Socket('/'))  # Register class Socket

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# rest API config
api = Api(app)
api.init_app(app)
api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
api.add_resource(File, '/file')
api.add_resource(List, '/list')
api.add_resource(User, '/user/<string:username>')
api.add_resource(Friend, '/friend/<int:id>', '/friend')
api.add_resource(PendingFriend, '/pending_friend/<int:id>', '/pending_friend')

# Static config
blueprint = Blueprint('site', __name__, static_folder='files')
app.register_blueprint(blueprint)

# TEST
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
