from flask import Flask
from models import db
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
