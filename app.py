from flask import Flask
from flask_restful import Resource, Api
from ressources.auth.register import Register
from models import db
import os

# Flask config
app = Flask(__name__)
app.config['DEBUG'] = os.environ.get('DEBUG')

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# API config
api = Api(app)
api.add_resource(Register, '/auth/register')
api.init_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
