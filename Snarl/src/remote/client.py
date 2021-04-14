import sys, os, argparse, json, socket
from constants import EJECT, END_GAME, END_LEVEL, EXIT, INVALID, KEY, OK, P_UPDATE, START_LVL, TYPE, WELCOME

from utilities import receive_msg, send_msg
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from player.localPlayer import LocalPlayer


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', dest='address', action='store', default='127.0.0.1', help='Address to start listing for connections')
parser.add_argument('-p', '--port', dest='port', action='store', type=int, default=45678, help='Port to start listing for connections')


class Client:
    __socket = None

    def __init__(self, host, port):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((host, port))
        self.player = None

    def __send(self, msg):
        send_msg(self.__socket, msg, 'server')

    def __receive(self):
        return receive_msg(self.__socket, 'server')
    
    @staticmethod
    def is_name_msg(req):
        return type(req) == str and req == 'name'
    
    @staticmethod
    def is_server_welcome(req):
        return type(req) == dict and WELCOME == req[TYPE]
    
    @staticmethod
    def is_start_level(req):
        return type(req) == dict and START_LVL == req[TYPE]

    @staticmethod
    def is_player_update(req):
        return type(req) == dict and P_UPDATE == req[TYPE]

    @staticmethod
    def is_player_move(req):
        return type(req) == dict and 'move' == req[TYPE]
    
    @staticmethod
    def is_result(req):
        valid_results = [OK, KEY, EXIT, EJECT, INVALID]
        return type(req) == str and req in valid_results
    
    @staticmethod
    def is_end_level(req):
        return type(req) == dict and END_LEVEL == req[TYPE]

    @staticmethod
    def is_end_game(req):
        return type(req) == dict and END_GAME == req[TYPE]


    def run(self):
        
        while True:
            data = self.__receive()
            if not data:
                break
            req = json.loads(data)

            #Receive server welcome and prompt for name

            #Receive start_level

            #Receive player_update msg

            #Receive "move" prompt player for move, and receive result

            #Receive end_level

            #Receive end_game
            



        self.__socket.close()
