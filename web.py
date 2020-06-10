# from app import create_app
import os

port = int(os.environ.get("PORT", 5000))

from flask import Flask

def create_app(environment="prod"):
    # 
    application = Flask(__name__)
    application.config.from_object('settings')

    # cors...

    # db...

    # Upload Blueprint
    from app.views.upload import upload_blueprint
    application.register_blueprint(upload_blueprint)

    return application


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=True)
