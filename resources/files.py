import sys
import glob
from flask import request
from flask_restful import Resource, reqparse, fields, marshal
from werkzeug.utils import secure_filename
from common.auth import authenticate
from models import db
from models import File as F
import os

ALLOWED_EXTENSIONS = {'gif', 'png', 'jpg', 'jpeg', 'mp4', 'mp3'}
FILE_DIR = "files/"
SAVE_DIR = os.path.join(os.path.dirname(__file__) + '/../' + FILE_DIR)


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


file_fields = {
    'path': fields.String
}


class File(Resource):
    # Protected endpoint
    method_decorators = [authenticate]

    # Upload
    def post(self, user):
        if 'file' not in request.files:
            return {'message': 'Required field file'}, 400
        file = request.files['file']
        if file.filename == '':
            return {'message', 'file is empty'}, 400
        if not allowed_file(file.filename):
            return {'message': 'file extension not allowed'}, 400
        filename = secure_filename(user.username + '-' + file.filename)

        # Saving file into files/ folder
        file.save(SAVE_DIR + filename)

        # Create object File
        new_file = F(user_id=user.id, path=filename)

        # Commit object in database
        db.session.add(new_file)
        db.session.commit()
        return {}

    # Get
    def get(self, user):
        all_files = user.files
        for i in user.friends:
            all_files += i.files
        return marshal(all_files, file_fields)


class Download(Resource):
    # Protected endpoint
    method_decorators = [authenticate]

    def get(self, user, filename):
        print(filename, file=sys.stderr)
        return {'files': filename}
