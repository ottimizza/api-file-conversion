class IllegalArgumentsException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Not enough storage space.'

class HttpErrorResponse:

    def __init__(self, exception):
        super().__init__()

    def json(self):
        return json.dumps({
            "error": ""
        })
