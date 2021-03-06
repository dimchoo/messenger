from argparse import ArgumentParser
from datetime import datetime
import json
from socket import socket, AF_INET, SOCK_STREAM

import yaml


parser = ArgumentParser()
parser.add_argument('-c', '--config', type=str, required=False, help='Sets config file path')
args = parser.parse_args()


default_config = {
    'host': '127.0.0.1',
    'port': 8000,
    'buffer_size': 1024
}

host, port, buffer_size = (
    default_config.get('host'),
    default_config.get('port'),
    default_config.get('buffer_size')
)

if args.config:
    with open(args.config, 'r', encoding='utf-8') as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(file_config)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((host, port))

print('Client was started...')

action = input('Enter action: ')
data = input('Enter data: ')

request = {
    'action': action,
    'time': datetime.now().timestamp(),
    'data': data
}

str_request = json.dumps(request)

client_socket.send(str_request.encode())

print(f'Client sent data:\n{str_request}')

server_byte_response = client_socket.recv(buffer_size)

print(f'Response from server:\n{server_byte_response.decode()}')

