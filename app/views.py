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


@app.errorhandler(HTTP_404_NOT_FOUND)
def not_found(error):
    return render_template('/exceptions/404.html'), HTTP_404_NOT_FOUND


@app.errorhandler(HTTP_405_METHOD_NOT_ALLOWED)
def not_allowed(error):
    return render_template('/exceptions/405.html'), HTTP_405_METHOD_NOT_ALLOWED


@app.route('/')
def redirect_to_download():
    return redirect(url_for('download_view'))


@app.route('/download/')
def download_view():
    return render_template('/pages/download.html'), HTTP_200_OK


@app.route('/upload/')
def upload_view():
    return render_template('/pages/upload.html'), HTTP_200_OK


@app.route('/download-file-by-code/<int:file_id>', methods=['GET'])
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

    session.setdefault('codes', []).append(record.code)

    response = jsonify({
        'message': 'File successfully uploaded',
        'file': record.to_dict(rules=('-path',)),
    })

    return response, HTTP_201_CREATED
