import sys, os, argparse, time, json
import socket
from pathlib import Path
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from remote.messages import Welcome
from constants import MAX_PLAYERS
from controller.controller import parse_levels
from game.gameManager import GameManager

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--levels', dest='levels', action='store', default='snarl.levels', help="Location of local levels file")
parser.add_argument('-c', '--clients', dest='clients', action='store', type=int, default=1, help='Number of players')
parser.add_argument('-w', '--wait', dest='wait', action='store', type=int, default=20, help='Number of seconds to wait for next player to connect before connection timeout')
parser.add_argument('-s', '--start', dest='start', action='store', type=int, default=1, help='Start level. Not 0 indexed')
parser.add_argument('-o', '--observe', dest='observe', action='store_true', default=False, help='Whether to return observer view of the ongoing game.')
parser.add_argument('-a', '--address', dest='address', action='store', default='127.0.0.1', help='Address to start listing for connections')
parser.add_argument('-p', '--port', dest='port', action='store', type=int, default=45678, help='Port to start listing for connections')


def __valid_clients_num(no_clients):
    return no_clients <= MAX_PLAYERS

def __send_server_welcome(connection, server_addr):
    info = '(Enesseand) server_address: {}'.format(server_addr)
    welcome_msg = Welcome(info)
    formatted_msg = json.dumps(welcome_msg)
    connection.send(formatted_msg.encode('utf-8'))

def main(args):
    if not __valid_clients_num(args.clients):
        print('Invalid number of clients. Please enter a number between 1 and {}'.format(MAX_PLAYERS))
        exit()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (args.address, args.port)
    server_socket.bind(server_addr)
    server_socket.listen(MAX_PLAYERS)
    server_socket.settimeout(float(args.wait))
    no_clients = args.clients

    levels_file = Path(args.levels).read_text()
    levels_list = parse_levels(levels_file)

    clients = []
    start = time.perf_counter()
    while len(clients) < no_clients:
        start = time.perf_counter()
        try:
            conn, addr = server_socket.accept()
            __send_server_welcome(conn, server_addr[0])
        except socket.timeout:
            end = time.perf_counter()
            dur = int(end - start)
            print('Timeout: {} seconds have passed since last player connected'.format(dur))
            server_socket.close()
            exit()





if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
