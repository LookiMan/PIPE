from flask import abort
from flask import jsonify
from flask import render_template
from flask import redirect
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
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


@app.errorhandler(HTTP_404_NOT_FOUND)
def not_found(error):
    return render_template('/exceptions/404.html'), HTTP_404_NOT_FOUND


@app.errorhandler(HTTP_405_METHOD_NOT_ALLOWED)
def not_allowed(error):
    return render_template('/exceptions/405.html'), HTTP_405_METHOD_NOT_ALLOWED


@app.route('/')
def redirect_to_download():
    return redirect(url_for('download_view'))


@app.route('/upload/')
def upload_view():
    return render_template('/pages/upload.html'), HTTP_200_OK


@app.route('/download/')
def download_view():
    return render_template('/pages/download.html'), HTTP_200_OK


@app.route('/upload-file/', methods=['POST'])
def upload_controller():
    if request.method != 'POST':
        return abort(HTTP_405_METHOD_NOT_ALLOWED)

    file = request.files.get('file')

    if not file:
        return 'File not selected', HTTP_400_BAD_REQUEST

    try:
        record = storage.save(file.stream, file.filename)
    except (DataError, IntegrityError, ProgrammingError, SQLAlchemyError, Exception) as e:
        app.logger.exception(e)
        return 'Unknown error', HTTP_500_INTERNAL_SERVER_ERROR

    session.setdefault('ids', []).append(record.id)

    files_schema = FileSchema(is_files_owner=True)

    response = jsonify({
        'message': 'File successfully uploaded',
        'file': files_schema.dump(record),
    })

    return response, HTTP_201_CREATED


@app.route('/download-file/<int:file_id>', methods=['GET'])
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
        directory=item.directory,
        path=item.path,
        as_attachment=True,
    )


@app.route('/remove-file/<int:file_id>', methods=['DELETE'])
def remove_controller(file_id):
    try:
        item = db.session.query(File)\
            .filter(File.id == file_id).first()
    except (ProgrammingError, SQLAlchemyError) as e:
        app.logger.exception(e)
        return 'Unknown error', HTTP_500_INTERNAL_SERVER_ERROR

    if not item:
        return 'File not found', HTTP_404_NOT_FOUND

    db.session.delete(item)
    db.session.commit()

    return 'File successfully removed', HTTP_204_NO_CONTENT


@app.route('/all-uploaded-files/', methods=['GET'])
def all_uploaded_files_controller():
    files_schema = FileSchema(many=True)

    try:
        items = db.session.query(File)
    except (ProgrammingError, SQLAlchemyError) as e:
        app.logger.exception(e)
        items = []

    return files_schema.dump(items), HTTP_200_OK


@app.route('/user-uploaded-files/', methods=['GET'])
def user_uploaded_files_controller():
    files_schema = FileSchema(is_files_owner=True, many=True)

    try:
        items = db.session.query(File)\
            .filter(File.id.in_(session.get('ids', [])))
    except (ProgrammingError, SQLAlchemyError, Exception) as e:
        app.logger.exception(e)
        items = []

    return files_schema.dump(items), HTTP_200_OK
