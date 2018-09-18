from . import api
from flask_restplus import Resource
from werkzeug.datastructures import FileStorage
from flask import request
from flask import current_app
import os
import time

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


@api.route('/upload/')
@api.expect(upload_parser)
class Upload(Resource):
    def post(self):
        uploaded_file = request.files['file']
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.filename)[-1]
            filename = str(time.time()).replace('.', '') + ext
            file = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file)
            return {'old_name': uploaded_file.filename,
                    'new_name': filename}, 201
        else:
            return {'old_name': None}, 400
