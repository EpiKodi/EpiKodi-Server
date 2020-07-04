from flask import request
from flask_restful import Resource, reqparse, fields, marshal
from werkzeug.utils import secure_filename
import os

import sys

ALLOWED_EXTENSIONS = {'png', 'jpg', 'mp4', 'mp3'}
FILE_DIR = "files/"

def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Upload(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'message': 'Required field file'}, 400
        file = request.files['file']
        if file.filename == '':
            return {'message', 'Required field file'}, 400
        if not allowed_file(file.filename):
            return {'message': 'file extension not allowed'}, 400
        file.save(FILE_DIR + secure_filename(file.filename))
        return {}
