import os
from flask import abort, Blueprint, g, jsonify, render_template, request, Response, send_file, current_app, after_this_request
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

# from app.exceptions import IllegalArgumentsException

from settings import UPLOAD_FOLDER, UPLOAD_ALLOWED_EXTENSIONS

import app.views.utils as view_utilities

from conversion import PDFConverter
from conversion.config import PDFConverterConfig


upload_blueprint = Blueprint('upload', __name__)


@upload_blueprint.errorhandler(Exception)
def illegal_arguments_exception_handler(exception):
    return {"error": "illegal_arguments"}


@upload_blueprint.route('/api/v1/conversions/upload', methods=['POST'])
@cross_origin()
def upload_files():
    # inicialização das mandingas...
    files = []
    opts = {}

    # pegamos o(s) arquivo(s) enviados, tanto se
    # enviar apenas um quando multiplos, esse é obrigatório!!!  *** CRIAR CUSTOM EXCEPTION ***
    if 'file' in request.files:
        files = [request.files['file']]
    elif 'file[]' in request.files:
        files = request.files.getlist("file[]")
    else:
        raise Exception("No file provided!")

    # opts: objeto JSON contendo todas as configuracoes necessarias
    # para a conversão de pdf para csv.
    # caso o mesmo não seja enviado utiliza uma config default. :)
    if 'opts' in request.form:
        import json
        opts = json.loads(request.form['opts'])
    else:
        opts = PDFConverterConfig.default_opts()

    # pegamos apenas o primeiro por enquanto... avoiding timeouts (,:
    f = files[0]

    # garantindo que o arquivo gravado em disco não vai dar problema
    filename = secure_filename(f.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    # salvando no diretorio de upload.
    f.save(filepath)

    # criacao de um arquivo temporario para nao termos mais
    # a necessidade de exclusão do mesmo apos o download
    tempfile = view_utilities.create_tempfile(True)

    # Conversão de Arquivos...
    #
    # instancia do conversor de pdf.
    converter = PDFConverter(filepath, PDFConverterConfig(**opts))

    # começa a conversão do pdf para csv.
    converter.parse()

    # constroi o csv a partir das celulas extraidas do pdf.
    converter.write(tempfile)

    # caminho para o arquivo convertido (.csv)
    outpath = converter.csv_file

    # apos a execucao exclui o arquivo... se existir ainda e.e
    @after_this_request
    def delete_outpath(response):
        try:
            os.remove(outpath)
        except Exception as error:
            print("Error removing or closing downloaded file handle")
        return response

    return send_file(outpath, attachment_filename='out.csv')
