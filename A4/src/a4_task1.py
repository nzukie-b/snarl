#!/usr/bin/env python

import socket
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('tcp_addr', type=str, nargs='?', help='Server address to connect to.', default='127.0.0.1')
parser.add_argument('port', type=int, nargs='?', help='Port to connect to', default=8000)
parser.add_argument('username', type=str, nargs='?', help='How the server will address the user', default='Glorifrir Flintshoulder')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def json_encode(obj):
    return json.dumps(obj).encode('utf-8')

def main():
    args = parser.parse_args()
    server_addr = (args.tcp_addr, args.port)
    s.connect(server_addr)
    s.sendall(json_encode(args.username))
    session_id = s.recv(2048)
    ## Username of session_id ?
    print(['the server will call me', args.username])
    while True:
        


    print(args)
    s.close()

if __name__ == '__main__':
    main()

