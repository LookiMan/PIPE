from argparse import ArgumentParser

from app import app
from app.utils import get_ip


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

    app.run(host='0.0.0.0', port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
