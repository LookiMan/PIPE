from os import path
from secrets import token_hex

from app.models import File


class Storage:
    def __init__(self, location, db):
        self.location = location
        self.db = db

    def _create_alias(self, filename):
        return f'{token_hex(nbytes=16)}.{filename}'

    def _save_file(self, fp, path):
        with open(path, mode='wb') as file:
            file.write(fp.read())

    def save(self, fp, filename):
        full_path = path.join(self.location, self._create_alias(filename))

        self._save_file(fp, full_path)

        file = File(name=filename, path=full_path)

        self.db.session.add(file)
        self.db.session.commit()

        return file
