import socket


PIPE_LUI_HEADER = 'PP-Last-Update-Id'


def get_ip():
    return socket.gethostbyname(socket.gethostname())


def add_last_update_id_to_headers(response, id):
    response.headers[PIPE_LUI_HEADER] = id
    return response


def filter_last_update_id(value):
    return int(value) if value and value.isdigit() else 0
