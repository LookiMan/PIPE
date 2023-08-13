from flask import Flask
from flask.logging import logging
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from .storage import Storage


logging.basicConfig(filename='app.log', level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
ma = Marshmallow(app)

Session(app)

with app.app_context():
    storage = Storage(app, db)

from .commands import command_cli # NOQA
app.register_blueprint(command_cli)

from .views import app_cli # NOQA
app.register_blueprint(app_cli)
