from os import path

from colorama import Fore
from flask import abort
from flask import request
from flask import render_template
from flask import session
from flask import send_from_directory
from flask import redirect
from flask import url_for
from flask_api.exceptions import NotFound
from flask_api.status import HTTP_200_OK
from flask_api.status import HTTP_201_CREATED
from flask_api.status import HTTP_404_NOT_FOUND
from flask_api.status import HTTP_405_METHOD_NOT_ALLOWED

from app import app


@app.errorhandler(HTTP_404_NOT_FOUND)
def not_found(error):
    return render_template('/exceptions/404.html'), HTTP_404_NOT_FOUND


@app.route('/')
def redirect_to_download():
    return redirect(url_for('download_view'))


@app.route('/download/')
@app.route('/download/<string:code>')
def download_view(code=None):
    if code and not session.get(code):
        raise NotFound()
    return render_template('/pages/download.html', context={'code': code}), HTTP_200_OK


@app.route('/upload/')
def upload_view():
    return render_template('/pages/upload.html'), HTTP_200_OK


@app.route('/download-file-by-code/<string:code>', methods=['GET'])
def download_controller(code):
    item = session.get(code)
    if not item:
        raise NotFound()

    return send_from_directory(
        directory=item.directory,
        path=item.path,
        as_attachment=True,
    )


@app.route('/upload-file/', methods=['POST'])
def upload_controller():
    if request.method != 'POST':
        return abort(HTTP_405_METHOD_NOT_ALLOWED)

    folder = app.config['UPLOAD_FOLDER']
    file = request.files.get('file')
    file.save(path.join(folder, file.filename))

    print(
        Fore.GREEN + f' * File: {file.filename} successfully downloaded in: {folder}'
    )

    return 'File successfully uploaded', HTTP_201_CREATED
