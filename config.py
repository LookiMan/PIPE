from os import getenv

from dotenv import load_dotenv


load_dotenv()

HOST = '0.0.0.0'
UPLOAD_FOLDER = './uploads/'

SECRET_KEY = getenv('SECRET_KEY')

SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = './.flask_session/'

SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite.db'
