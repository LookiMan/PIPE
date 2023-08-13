from flask import Blueprint

from .. import db
from .. import storage
from ..models import File


command_cli = Blueprint('command', __name__)


@command_cli.cli.command('clear')
def remove_all_files():
    files = db.session.query(File)

    for file in files:
        if storage.is_exists(file.alias):
            storage.remove(file.alias)

        db.session.delete(file)
    db.session.commit()

    print('Files removed successfully!')
