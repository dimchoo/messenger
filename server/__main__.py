from argparse import ArgumentParser
from socket import socket, AF_INET, SOCK_STREAM

import yaml


parser = ArgumentParser()
parser.add_argument(
    '-c', '--config',
    type=str,
    required=False,
    help='Sets config file path'
)
args = parser.parse_args()

default_config = {
    'host': '127.0.0.1',
    'port': 8000,
    'connection_number': 5,
    'buffer_size': 1024
}

if args.config:
    with open(args.config, 'r', encoding='utf-8') as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(file_config)

host, port, connection_number, buffer_size = (
    default_config.get('host'),
    default_config.get('port'),
    default_config.get('connection_number'),
    default_config.get('buffer_size')
)

try:
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(connection_number)

    print(f'Server was started with {host}:{port}...')

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Server was connected with {client_address[0]}:{client_address[1]}...')
        client_byte_request = client_socket.recv(buffer_size)
        print(f'Client sent request:\n{client_byte_request.decode()}')
        client_socket.send(client_byte_request)
        print(f'Server sent request:\n{client_byte_request.decode()}')
        client_socket.close()
except KeyboardInterrupt:
    print('\nServer was shutdown.')
