from colorama import init
from dotenv import load_dotenv
from flask import Flask
from flask.logging import logging
from flask_session import Session


load_dotenv()
init(autoreset=True)

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config.from_object('config')
Session(app)

from app import views # NOQA
