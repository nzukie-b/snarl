#!/usr/bin/env python

import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('tcp_addr', type=str, nargs='?', help='Server address to connect to.', default='127.0.0.1')
parser.add_argument('port', type=int, nargs='?', help='Port to connect to', default=8000)
parser.add_argument('username', type=str, nargs='?', help='How the server will address the user', default='Glorifrir Flintshoulder')

def main():
    args = parser.parse_args()
    
    print(args)


if __name__ == '__main__':
    main()

