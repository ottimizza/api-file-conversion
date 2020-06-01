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
