import sys
import glob
from flask import request, send_file
from flask_restful import Resource, reqparse, fields, marshal
from werkzeug.utils import secure_filename
from common.auth import authenticate, get_user
from models import db
from models import File as F
import os
import uuid
from pathlib import Path

ALLOWED_EXTENSIONS = {'gif', 'png', 'jpg', 'jpeg', 'mp4', 'mp3'}
FILE_DIR = "files/"
SAVE_DIR = os.path.join(os.path.dirname(__file__) + '/../' + FILE_DIR)


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


file_fields = {
    'id': fields.String,
    'filename': fields.String,
    'user': fields.String,
    'extension': fields.String
}


class File(Resource):
    # Protected endpoint
    method_decorators = [authenticate]

    # Upload
    def post(self, user):
        if 'file' not in request.files:
            return {'error': 'Required field file'}, 400
        file = request.files['file']
        if file.filename == '':
            return {'error', 'file is empty'}, 400
        if not allowed_file(file.filename):
            return {'error': 'file extension not allowed'}, 400

        # Create subdirectory if not exist
        Path(SAVE_DIR + user.username).mkdir(parents=True, exist_ok=True)

        # Saving file into files/ folder
        filename = secure_filename(file.filename)
        file.save(SAVE_DIR + user.username + '/' + filename)

        # Create object File
        index = filename.rindex('.')
        extension = filename[index + 1:]
        new_file = F(id=uuid.uuid4().hex, user_id=user.id, filename=filename, user=user.username, extension=extension)

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


class FileManager(Resource):
    # Protected endpoint for delete method
    method_decorators = {'delete': [authenticate]}

    def get(self, filename):
        token = request.args.get('token')
        user = get_user(token)

        # Check if the user can access to the file
        all_files = user.files
        for i in user.friends:
            all_files += i.files
        all_id = []
        for i in all_files:
            all_id.append(i.id)
        if filename not in all_id:
            return {'error': 'You don\'t have access to the required file'}, 400

        # Get file object from filename
        f = None
        for i in all_files:
            if i.id == filename:
                f = i

        # Return file data
        filename = SAVE_DIR + f.user + '/' + f.filename
        return send_file(filename, mimetype=f.extension)

    def delete(self, user, filename):
        # Get File object
        f = None
        for i in user.files:
            if i.id == filename:
                f = i
        
        # Error handler
        if f is None:
            return {'error': 'file not found'}, 400

        # Remove and commit changes
        db.session.delete(f)
        db.session.commit()
        return {}
