import os
from flask import abort, Blueprint, g, jsonify, render_template, request, Response
from werkzeug.utils import secure_filename

from settings import UPLOAD_FOLDER, UPLOAD_ALLOWED_EXTENSIONS

upload_blueprint = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in UPLOAD_ALLOWED_EXTENSIONS


@upload_blueprint.route('/api/v1/conversions/upload', methods=['POST'])
@cross_origin()
def upload_files():
    files = []
    details = { "files": [] }

    # check if the post request has the file part
    if 'file' in request.files:
        files = [ request.files['file'] ]
    elif 'file[]' in request.files:
        files = request.files.getlist("file[]")
    else:
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

