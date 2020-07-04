from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from resources.auth import Register, Login
from resources.files import Upload
from models import db
from cryptography.fernet import Fernet
import os

# Flask config
app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = os.environ.get('DEBUG')
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__)) + '/files'

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# API config
api = Api(app)
api.init_app(app)
api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
api.add_resource(Upload, '/file/upload')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
