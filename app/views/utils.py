


def allowed_filename(filename, extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in extensions


def create_tempfile(filename):
    pass