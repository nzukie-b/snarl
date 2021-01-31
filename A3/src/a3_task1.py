import socket
import sys
import os
import sys
import json
# Adding the A2 directory to allow importing the file without moving/copying it
currentdir = os.path.dirname(os.path.realpath(__file__))
a3_dir = os.path.dirname(currentdir)
root_dir = os.path.dirname(a3_dir)
a2_dir = root_dir + '/A2/src'
sys.path.append(a2_dir)
from a2 import serialize_output, streaming_iterload


# Create a TCP socket and listen at port 55555
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ('localhost', 8081)
socket.bind(server_addr)
socket.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_addr = socket.accept()
    parsed_values = []
    print('Listening ')
    while True:
        chunk = connection.recv(1024).decode('utf-8').rstrip()
        if chunk == 'END':
            res = serialize_output(parsed_values, 'sum')
            print(res)
            connection.sendall(res.encode('utf-8'))
            break;
        else :
            for o in streaming_iterload(chunk):
                if o:
                    parsed_values.append(o)
    break

connection.close()