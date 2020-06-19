# from app import create_app
from flask import Flask
from flask_cors import CORS, cross_origin

import os

port = int(os.environ.get("PORT", 5000))


# def create_app(environment="prod"):
#
application = Flask(__name__)
application.config.from_object('settings')

# cors...
cors = CORS(application)


# db...

# Upload Blueprint
from app.views.upload import upload_blueprint
application.register_blueprint(upload_blueprint)

# return application



if __name__ == "__main__":
    # app = create_app()
    application.run(host="0.0.0.0", port=port, debug=True, threaded=True)
