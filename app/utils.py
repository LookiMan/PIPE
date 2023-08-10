import socket
import string
import random
from dataclasses import dataclass

import colorama
import qrcode


@dataclass
class FileItem:
    directory: str
    path: str


def get_ip():
    return socket.gethostbyname(socket.gethostname())


def generate_short_code(length=4):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_qr_code(text):
    colorama.init()

    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10,
                       border=4)
    qr.add_data(text)
    qr.make()
    qr.print_tty()
