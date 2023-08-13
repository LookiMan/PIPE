from os import path
from os import remove as os_remove
from secrets import token_hex

from accessify import private

from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError

from app.models import File
from app.models import StorageLastUpdate


class Storage:
    _last_update_id = None
    _upload_folder = None

    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.upload_folder = app.config['UPLOAD_FOLDER']
        self.init_last_update_id()

    @property
    def last_update_id(self):
        return self._last_update_id

    @private
    @last_update_id.setter
    def last_update_id(self, value):
        self._last_update_id = value

    @property
    def upload_folder(self):
        return self._upload_folder

    @private
    @upload_folder.setter
    def upload_folder(self, value):
        self._upload_folder = value

    @private
    def init_model(self):
        try:
            model = self.db.session.query(StorageLastUpdate).one()
        except NoResultFound:
            model = StorageLastUpdate()
            self.db.session.add(model)
            self.db.session.commit()
        except (SQLAlchemyError, MultipleResultsFound) as e:
            self.app.logger.exception(e)
            raise e
        return model

    @private
    def init_last_update_id(self):
        self.last_update_id = self.init_model().value

    @private
    def increase_last_update_id(self):
        self.last_update_id += 1

    @private
    def update_last_id(self):
        self.increase_last_update_id()
        model = self.init_model()
        model.value = self.last_update_id
        self.db.session.commit()

    @private
    def create_alias(self, filename):
        return f'{token_hex(nbytes=16)}.{filename}'

    @private
    def save_file(self, fp, path):
        with open(path, mode='wb') as file:
            file.write(fp.read())

    def save(self, fp, filename):
        alias = self.create_alias(filename)
        full_path = path.join(self.upload_folder, alias)

        self.save_file(fp, full_path)

        file = File(name=filename, alias=alias)

        self.db.session.add(file)
        self.db.session.commit()

        self.update_last_id()

        return file

    def remove(self, filename):
        try:
            os_remove(path.join(self.upload_folder, filename))
        except (FileNotFoundError, PermissionError) as e:
            self.app.logger.exception(e)

        self.update_last_id()

    def is_exists(self, filename):
        return path.join(self.upload_folder, filename)
