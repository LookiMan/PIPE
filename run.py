from argparse import ArgumentParser
from os import path

from colorama import Fore
from flask import session

from app import app
from app.utils import generate_short_code
from app.utils import generate_qr_code
from app.utils import get_ip
from app.utils import FileItem


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '--port', '-p',
        action='store',
        default=5000,
        type=int,
        nargs='?',
        help='Specify alternate port [default: 5000]')
    parser.add_argument(
        '--filename', '-f',
        action='store',
        default=None,
        type=str,
        help='File name to distributing [optional]')
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        default=False,
        help='Specify debug mode [default: False]'
    )
    args = parser.parse_args()

    ip = get_ip()

    print(' * ===========================================')
    print(' * Server IP address:', f'{ip} PORT: {args.port}')
    print(' * Control panel URL:', f'http://{ip}:{args.port}')
    print(' * ===========================================')

    if args.filename and path.isfile(args.filename):
        code = generate_short_code()
        link = f'http://{ip}:{args.port}/download/{code}'

        generate_qr_code(link)

        print(Fore.GREEN + ' * ============================')
        print(Fore.GREEN + ' * Download link:', Fore.CYAN + link)
        print(Fore.GREEN + ' * Download code:', Fore.CYAN + code)
        print(Fore.GREEN + ' * ============================')

        session[code] = FileItem(
            path.dirname(args.filename),
            path.basename(args.filename),
        )

    app.run(host='0.0.0.0', port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
