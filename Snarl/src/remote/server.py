import sys, os, argparse, time, json, math
import socket
from pathlib import Path
from typing import List
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from model.gamestate import GameState
from player.remotePlayer import RemotePlayer
from coord import Coord
from utilities import update_remote_players, send_msg, receive_msg
from remote.messages import EndGame, EndLevel, PlayerScore, StartLevel, Welcome
from constants import A_WIN, CONN, EJECT, END_LEVEL, EXIT, GAME_END, INFO, INVALID, KEY, LEVEL_END, MAX_PLAYERS, NAME, GHOST, OK, P_UPDATE, STATUS, VALID_MOVE, ZOMBIE
from controller.controller import parse_levels
from game.gameManager import GameManager
from view.view import render_state

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

def __send_server_welcome(connection: socket.SocketType, server_addr):
    info = '(Enesseand) server_address: {}'.format(server_addr)
    welcome_msg = Welcome(info)
    formatted_msg = json.dumps(welcome_msg.__dict__)
    connection.sendall(formatted_msg.encode('utf-8'))

def __request_client_name(connection: socket.SocketType, clients):
    '''Send name prompt to client client connection. If the name is already taken it will attempt to reprompt 4 times before moving on.'''
    msg = "name"
    msg = json.dumps(msg)
    names = []
    client_info = {NAME: None, CONN: connection}
    for client in clients:
        names.append(client)
    for i in range(4):
        connection.sendall(msg.encode('utf-8'))
        client_name = receive_msg(connection, 'client')
        # client_name = connection.recv(4096).decode('utf-8')
        if client_name not in names:
            client_info[NAME] = client_name
            break
    return client_info

def __wait_for_client_connections(server_socket: socket.SocketType, server_addr, no_clients, timeout):
    '''Sets the timeout and waits for client connections. If the socket timesout the sever closes sockets and exits'''
    server_socket.settimeout(float(timeout))
    clients = []
    start = time.perf_counter()
    while len(clients) < no_clients:
        start = time.perf_counter()
        try:
            conn, addr = server_socket.accept()
            __send_server_welcome(conn, server_addr[0])
            client_info = __request_client_name(conn, clients)
            clients.append(client_info)
        except socket.timeout:
            end = time.perf_counter()
            dur = int(end - start)
            # Should we close client connections here?
            for client in clients:
                client[CONN].close()
            print('Timeout: {} seconds have passed since last player connected'.format(dur))
            server_socket.close()
            exit()
    return clients
    
def __close_invalid_clients(clients):
    '''Goes throgh clients, and closes any connections that did not provided a valid name'''
    for client in clients:
        if client[NAME] == None:
            client[CONN].close()

def __register_players(gm, clients):
    for client in clients:
        gm.register_player(client[NAME], client[CONN])

def __register_adversaries(gm: GameManager, no_levels):
    num_zombies = math.floor(no_levels / 2) + 1
    num_ghosts = math.floor((no_levels - 1) / 2)
    for ii in range(num_zombies):
        gm.register_adversary('zombie: {}'.format(ii), ZOMBIE, remote=True)
    for ii in range(num_ghosts):
        gm.register_adversary('ghost: {}'.format(ii), GHOST, remote=True)

def __send_level_start(no_level, clients):
    names = [client[NAME] for client in clients]
    start_lvl_msg = StartLevel(no_level, names)
    msg = json.dumps(start_lvl_msg.__dict__)
    for client in clients:
        client[CONN].sendall(msg.encode('utf-8'))
    
def __send_player_updates(gm):
    update_remote_players(gm.players, gm)


def __request_client_move(player: RemotePlayer, gm: GameManager, key, exits, ejects):
    msg = "move"
    msg = json.dumps(msg)
    conn = player.socket
    for i in range(4):
        send_msg(conn, msg, player.name)
        move_res = player.move_to_tile(gm)
        if move_res:
            player_obj = gm.get_player_actor(player.name)
            if move_res[VALID_MOVE] and move_res[INFO].traversable:
                res = gm.apply_player_item_interaction(player_obj, player_obj.pos)
                if res:
                    if res == KEY:
                        key = player.name
                        move_msg = json.dumps(res)
                    elif res == EXIT:
                        exits.append(player.name)
                        move_msg = json.dumps(res)
                elif move_res[EJECT]:
                    ejects.append(player.name)
                    move_msg = json.dumps(EJECT)
                else:
                    move_msg = json.dumps(OK)
                send_msg(conn, move_msg, player.name)
                return move_msg

        move_msg = json.dumps(INVALID)
        send_msg(conn, move_msg, player.name)

def __send_end_level(players: List[RemotePlayer], key, exits, ejects):
    '''Sends the level end message to all players '''
    key = 'null' if not key else key
    end_lvl = EndLevel(key, exits, ejects)
    msg = str(end_lvl)
    for player in players:
        send_msg(player.socket, msg, player.name)


def __send_end_game(players: List[RemotePlayer], player_scores: List[PlayerScore]):
    end_game = EndGame(player_scores)
    msg = str(end_game)
    for player in players:
        try:
            send_msg(player.socket, msg, player.name)
        except OSError:
            #player.socket is not a socket ?????
            pass

def __close_connections(players: List[RemotePlayer], server: socket.SocketType):
    for player in players:
        player.socket.close()
    server.close()

def __update_observer(observe: bool, state: GameState):
    if observe:
        render_state(state)

def main(args):
    if not __valid_clients_num(args.clients):
        print('Invalid number of clients. Please enter a number between 1 and {}'.format(MAX_PLAYERS))
        exit()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (args.address, args.port)
    server_socket.bind(server_addr)
    server_socket.listen(MAX_PLAYERS)
    
    no_clients = args.clients
    levels_file = Path(args.levels).read_text()
    levels_list = parse_levels(levels_file)
    start_level = args.start
    observe = args.observe

    clients = __wait_for_client_connections(server_socket, server_addr, no_clients, args.wait)
    __close_invalid_clients(clients)

    gm = GameManager()
    __register_players(gm, clients)
    __register_adversaries(gm, len(levels_list))
   
    gm.start_game(levels_list, start_level)
    
    __send_level_start(start_level, clients)
    __send_player_updates(gm)

    player_scores = [PlayerScore(player.name) for player in gm.players]
    key = None
    exits = []
    ejects = []
    while True:
        # Need to make copy of players and advs as gm modifies these during request_moves
        advs = [adv for adv in gm.adversaries]
        players = [p for p in gm.players]
        
        # print('p Turns', gm.player_turns)
        # print('a turns ', gm.adv_turns)
        for p in gm.player_turns:
            player = next(player for player in players if player.name == p)
            __request_client_move(player, gm, key, exits, ejects)
            __send_player_updates(gm)
            __update_observer(observe, gm.gamestate)
        # print('p Turns', gm.player_turns)
        # print('a turns ', gm.adv_turns)
        for adversary in gm.adv_turns:
            adv = next(adv for adv in advs if adv.name == adversary)
            adv.move_to_tile(gm)
            __update_observer(observe, gm.gamestate)
        level_over = gm.handle_level_over()
        game_over = gm.handle_game_over()
        # print(level_over)
        # print(game_over)
        if level_over[LEVEL_END]:
            __send_end_level(gm.players, key, exits, ejects)
            for p_score in player_scores:
                if p_score.name == key:
                    p_score.key += 1
                if p_score.name in exits:
                    p_score.exits += 1
                if p_score.name in ejects:
                    p_score.ejects += 1
            key = None
            exits = []
            ejects = []

            if game_over[GAME_END] or level_over[STATUS] == A_WIN:
                break

    __send_end_game(gm.players, player_scores)
    __close_connections(gm.players, server_socket)

                


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
