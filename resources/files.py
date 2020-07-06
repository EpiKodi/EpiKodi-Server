from flask import request
from flask_restful import Resource, reqparse, fields, marshal
from werkzeug.utils import secure_filename
from common.auth import authenticate
import os

import sys

ALLOWED_EXTENSIONS = {'gif', 'png', 'jpg', 'jpeg', 'mp4', 'mp3'}
FILE_DIR = "files/"
SAVE_DIR = os.path.join(os.path.dirname(__file__) + '/../' + FILE_DIR)

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        file.save(SAVE_DIR + secure_filename(file.filename))
        return {}
    
    # Get
    def get(self, user):
        return {}

import glob

class List(Resource):
    def get(self):
        return {'files': glob.glob(SAVE_DIR + '*')}
