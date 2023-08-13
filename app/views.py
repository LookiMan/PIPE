from os import path

from flask import after_this_request
from flask import render_template
from flask import redirect
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from flask import Blueprint
from flask_api.status import HTTP_200_OK
from flask_api.status import HTTP_201_CREATED
from flask_api.status import HTTP_204_NO_CONTENT
from flask_api.status import HTTP_400_BAD_REQUEST
from flask_api.status import HTTP_404_NOT_FOUND
from flask_api.status import HTTP_405_METHOD_NOT_ALLOWED
from flask_api.status import HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy.exc import DataError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.exc import SQLAlchemyError

from app import app
from app import db
from app import storage
from app.models import File
from app.schemes import FileSchema
from app.utils import add_last_update_id_to_headers
from app.utils import filter_last_update_id
from app.utils import PIPE_LUID_HEADER


app_cli = Blueprint('app', __name__)


@app_cli.errorhandler(HTTP_404_NOT_FOUND)
def not_found(error):
    return render_template('/exceptions/404.html'), HTTP_404_NOT_FOUND


@app_cli.errorhandler(HTTP_405_METHOD_NOT_ALLOWED)
def not_allowed(error):
    return render_template('/exceptions/405.html'), HTTP_405_METHOD_NOT_ALLOWED


@app_cli.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def internal_error(error):
    return render_template('/exceptions/500.html'), HTTP_500_INTERNAL_SERVER_ERROR


@app_cli.route('/')
def redirect_to_download():
    return redirect(url_for('app.download_view'))


@app_cli.route('/upload/')
def upload_view():
    return render_template('/pages/upload.html'), HTTP_200_OK


@app_cli.route('/download/')
def download_view():
    return render_template('/pages/download.html'), HTTP_200_OK


@app_cli.route('/upload-file/', methods=['POST'])
def upload_controller():
    file = request.files.get('file')

    if not file:
        return 'File not selected', HTTP_400_BAD_REQUEST

    try:
        record = storage.save(file.stream, file.filename)
    except (DataError, IntegrityError, ProgrammingError, SQLAlchemyError, Exception) as e:
        app.logger.exception(e)
        return 'Unknown error', HTTP_500_INTERNAL_SERVER_ERROR

    session.setdefault('ids', []).append(record.id)

    return 'File successfully uploaded', HTTP_201_CREATED


@app_cli.route('/download-file/<int:file_id>', methods=['GET'])
def download_controller(file_id):
    try:
        item = db.session.query(File)\
            .filter(File.id == file_id).first()
    except (ProgrammingError, SQLAlchemyError) as e:
        app.logger.exception(e)
        item = None

    if not item:
        return 'File not found', HTTP_404_NOT_FOUND

    return send_from_directory(
        directory=path.abspath(app.config['UPLOAD_FOLDER']),
        path=item.alias,
        as_attachment=True,
        download_name=item.name,
    )


@app_cli.route('/remove-file/<int:file_id>', methods=['DELETE'])
def remove_controller(file_id):
    try:
        item = db.session.query(File)\
            .filter(File.id == file_id).first()
    except (ProgrammingError, SQLAlchemyError) as e:
        app.logger.exception(e)
        return 'Unknown error', HTTP_500_INTERNAL_SERVER_ERROR

    if not item:
        return 'File not found', HTTP_404_NOT_FOUND

    if storage.is_exists(item.alias):
        storage.remove(item.alias)

    db.session.delete(item)
    db.session.commit()

    return 'File successfully removed', HTTP_204_NO_CONTENT


@app_cli.route('/all-uploaded-files/', methods=['GET'])
def all_uploaded_files_controller():
    @after_this_request
    def add_last_update_id_header(response):
        return add_last_update_id_to_headers(response, storage.last_update_id)

    files_schema = FileSchema(many=True)
    client_last_update_id = filter_last_update_id(request.headers.get(PIPE_LUID_HEADER))

    if client_last_update_id == storage.last_update_id:
        items = []
    else:
        try:
            items = db.session.query(File)\
                .order_by(File.id.desc())
        except (ProgrammingError, SQLAlchemyError) as e:
            app.logger.exception(e)
            items = []

    return files_schema.dump(items), HTTP_200_OK


@app_cli.route('/own-uploaded-files/', methods=['GET'])
def own_uploaded_files_controller():
    @after_this_request
    def add_last_update_id_header(response):
        return add_last_update_id_to_headers(response, storage.last_update_id)

    files_schema = FileSchema(is_files_owner=True, many=True)
    client_last_update_id = filter_last_update_id(request.headers.get(PIPE_LUID_HEADER))

    if client_last_update_id == storage.last_update_id:
        items = []
    else:
        try:
            items = db.session.query(File)\
                .filter(File.id.in_(session.get('ids', [])))\
                .order_by(File.id.desc())
        except (ProgrammingError, SQLAlchemyError, Exception) as e:
            app.logger.exception(e)
            items = []

    return files_schema.dump(items), HTTP_200_OK
