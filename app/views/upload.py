import os
from flask import abort, Blueprint, g, jsonify, render_template, request, Response, send_file
from flask_cors import cross_origin
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

@upload_blueprint.errorhandler(IllegalArgumentsException)
def illegal_arguments_exception_handler(exception):
    return { "error": "illegal_arguments" }

@upload_blueprint.route('/api/v1/conversions/upload', methods=['POST'])
@cross_origin()
def upload_files():
    details = { "files": [] }
    files = []

    if 'file' in request.files:
        files = [ request.files['file'] ]
    elif 'file[]' in request.files:
        files = request.files.getlist("file[]")
    else:
        raise IllegalArgumentsException("No file provided!")
        # return jsonify({"error": "illegal_arguments", "error_description": "No file provided!"})

    print("print getting first from array")

    f = files[0]

    print("setting up names")
    # files iteration and validation
    # for f in files:
    filename = secure_filename(f.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    print("saving files...")

    f.save(filepath)

    # create temporary file
    # tempfile = view_utilities.create_tempfile()
    # try: 
    #     # f.save(os.path.join(UPLOAD_FOLDER, filename))
    # finally:
    #     os.unlink(tempfile.name)
    #     tempfile.close()

    print("starting conversion...")

    # process the tmp file and returns a temporary csv 
    from conversion import PDFConverter, PDFConverterConfig
    from conversion.strategy import ParseStrategyA
    
    config = PDFConverterConfig()
    strategy = ParseStrategyA()

    outpath = PDFConverter(filepath, strategy, config) \
        .parse() \
        .write()

    return send_file(UPLOAD_FOLDER, attachment_filename='out.csv')

# if uploaded_file and allowed_file(uploaded_file.filename):
#     filename = secure_filename(uploaded_file.filename)
#     uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))
# return { "details": details }