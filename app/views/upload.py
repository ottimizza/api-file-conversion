import os
from flask import abort, Blueprint, g, jsonify, render_template, request, Response, send_file, current_app
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

from app.exceptions import IllegalArgumentsException

from settings import UPLOAD_FOLDER, UPLOAD_ALLOWED_EXTENSIONS

import app.views.utils as view_utilities

from conversion import PDFConverter
from conversion.config import PDFConverterConfig



upload_blueprint = Blueprint('upload', __name__)

@upload_blueprint.errorhandler(IllegalArgumentsException)
def illegal_arguments_exception_handler(exception):
    return { "error": "illegal_arguments" }


@upload_blueprint.route('/api/v1/conversions/upload', methods=['POST'])
@cross_origin()
def upload_files():
    files = []
    opts = {}

    if 'file' in request.files:
        files = [ request.files['file'] ]
    elif 'file[]' in request.files:
        files = request.files.getlist("file[]")
    else:
        raise IllegalArgumentsException("No file provided!")


    if 'opts' in request.form:
        import json
        opts = json.loads(request.form['opts'])
    else:
        opts = PDFConverterConfig.default_opts()
    
    f = files[0]

    filename = secure_filename(f.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    f.save(filepath)

    #
    # for f in files:
    # tempfile = view_utilities.create_tempfile()
    # try: 
    #     # f.save(os.path.join(UPLOAD_FOLDER, filename))
    # finally:
    #     os.unlink(tempfile.name)
    #     tempfile.close()
    # 

    # Conversão de Arquivos...
    #
    # instancia do conversor de pdf.
    converter = PDFConverter(filepath, PDFConverterConfig(**opts))

    # começa a conversão do pdf para csv.
    converter.parse()

    # constroi o csv a partir das celulas extraidas do pdf.
    converter.write()

    # caminho para o arquivo convertido (.csv)
    outpath = converter.csv_file

    return send_file(outpath, attachment_filename='out.csv')
