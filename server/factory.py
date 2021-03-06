import os
from rq import Queue

from flask import Flask
from flask_migrate import Migrate

from server.database import db
from server.login import login_manager
from server.mail import mail
from server.worker import conn
from server.socket import socketio
from server.sockets import sockets
from server.views import home
from server.views.upload import upload
from server.views.webapp import webapp

migrate = Migrate()


def create_dir_if_none(folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)


def create_app(override_config=None):
    app = Flask(__name__)

    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if override_config is not None:
        app.config.from_object(override_config)

    create_dir_if_none(app.config['PHOTO_UPLOAD_FOLDER'])

    db.init_app(app)

    migrate.init_app(app, db)

    login_manager.init_app(app)

    mail.init_app(app)

    socketio.init_app(app)

    app.task_queues = {
            'high': Queue('high', connection=conn),
            'default': Queue('default', connection=conn),
            'low': Queue('low', connection=conn)
            }

    app.register_blueprint(sockets)
    app.register_blueprint(home)
    login_manager.login_view = 'home.login'
    app.register_blueprint(upload)
    app.register_blueprint(webapp)
    return app
