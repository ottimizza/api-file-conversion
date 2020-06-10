import os
from flask import abort, Blueprint, g, jsonify, render_template, request, Response
from werkzeug.utils import secure_filename


from app.exceptions import IllegalArgumentsException

from settings import UPLOAD_FOLDER, UPLOAD_ALLOWED_EXTENSIONS

import app.views.utils as view_utilities


upload_blueprint = Blueprint('upload', __name__)

def get_request_files():
    files = []

    if 'file' in request.files:
        files = [ request.files['file'] ]
    elif 'file[]' in request.files:
        files = request.files.getlist("file[]")
    else:
        raise IllegalArgumentsException("No file provided!")

@upload_blueprint.errorhandler(app.exceptions.IllegalArgumentsException)
def illegal_arguments_exception_handler(exception):
    return 

@upload_blueprint.route('/api/v1/conversions/upload', methods=['POST'])
@cross_origin()
def upload_files():
    details = { "files": [] }

    try:
        files = get_request_files()
    except:
        return jsonify({"error": "illegal_arguments", "error_description": "No file provided!"})

    # files iteration and validation
    for f in files:
        filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, filename))

        details['files'].append(filename)
        

    # if uploaded_file and allowed_file(uploaded_file.filename):
    #     filename = secure_filename(uploaded_file.filename)
    #     uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))
        
    return { "details": details }
