from dotenv import load_dotenv
from flask import Flask
from flask.logging import logging
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from .storage import Storage


load_dotenv()

logging.basicConfig(filename='app.log', level=logging.DEBUG)

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object('config')

Session(app)

db.init_app(app)

storage = Storage(app.config['UPLOAD_FOLDER'], db)

from app import views # NOQA
