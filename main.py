import os
import argparse

from flask import (
    Flask,
    redirect,
    request,
    render_template,
    url_for,
    send_from_directory,
    abort
)
from flask.logging import logging
from colorama import init, Fore
from dotenv import load_dotenv

from utils import (
    generate_short_code,
    generate_qr_code,
    get_ip,
    FileItem,
)

load_dotenv()
init(autoreset=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./uploads/"

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

session = {}


@app.route("/")
def redirect_to_download():
    return redirect(url_for("download_view"))


@app.route("/download/")
def download_view():
    return render_template("download.html"), 200


@app.route("/download/<string:code>")
def download_with_code_view(code):
    if not session.get(code):
        return abort(404)

    context = {
        "code": code,
    }

    return render_template("download.html", context=context), 200


@app.route("/upload/")
def upload_view():
    return render_template("upload.html"), 200


@app.route("/downloader/<string:code>")
def download_controller(code):
    item = session.get(code)
    if not item:
        return {"success": False, "description": "По данному коду файлов не обнаружено"}, 404

    return send_from_directory(
        directory=item.directory,
        path=item.path,
        as_attachment=True,
    )


@app.route("/uploader/", methods=["POST"])
def upload_controller():
    if request.method != "POST":
        return abort(405)

    folder = app.config["UPLOAD_FOLDER"]
    file = request.files.get("file")
    file.save(os.path.join(folder, file.filename))

    print(
        Fore.GREEN + f" * Файл: {file.filename} успешно загружен в: {folder}"
    )

    return {"success": True, "description": "Файл успешно загружен"}


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", action="store",
                        default=5000, type=int,
                        nargs="?",
                        help="Specify alternate port [default: 5000]")
    parser.add_argument("--filename", "-f", action="store",
                        default=None, type=str,
                        help="File name to distributing [optional]")
    args = parser.parse_args()

    ip = get_ip()

    print(" * ===========================================")
    print(" * IP адрес сервера:", ip, "PORT:", args.port)
    print(" * URL адрес панели управления", f"http://{ip}:{args.port}")
    print(" * ===========================================")

    if args.filename and os.path.isfile(args.filename):
        code = generate_short_code()
        link = f"http://{ip}:{args.port}/download/{code}"

        generate_qr_code(link)

        print(Fore.GREEN + " * ============================")
        print(Fore.GREEN + " * Ссылка для скачивания:", Fore.CYAN + link)
        print(Fore.GREEN + " * Код для скачивания:", Fore.CYAN + code)
        print(Fore.GREEN + " * ============================")

        session[code] = FileItem(
            os.path.dirname(args.filename),
            os.path.basename(args.filename),
        )

    app.run(host="0.0.0.0", port=args.port, debug=False)


if __name__ == "__main__":
    main()
