


def allowed_filename(filename, extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in extensions


def create_tempfile(delete=False):
    import tempfile
    return tempfile.NamedTemporaryFile(delete=delete)


def zip(zipname, path):
    import os
    import zipfile

    zipf = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)

    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

    zipf.close()

    return zipname
