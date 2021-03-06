import json
import socket
import sys, os
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from common.player import Player
from remote.messages import RemoteActorUpdate
from utilities import receive_msg, send_msg, to_coord, to_point
from constants import TO

class RemotePlayer(Player):
    def __init__(self, socket: socket.SocketType, name=None, player_obj=None, layout=None, visible_tiles=None, actors=None, objects=None, inventory=None):
        super().__init__(name, player_obj=player_obj, layout=layout, visible_tiles=visible_tiles, actors=actors, objects=objects, inventory=inventory)
        self.socket = socket
        
    def move_to_tile(self, gm):
        """Move to a location within the visible tiles, if the same tile the player is currently on is
        selected as the move location then stay put as the move for that turn. Sends this info to game-manager to be
        handled."""
        data = self.__receive()
        move = json.loads(data)
        assert type(move) == dict and move[TO]
        return super().move_to_tile(to_coord(move[TO]), gm)

    def interact_with_tile_contents(self, current_tile_info):
        """Interact with the contents on the current tile if it exists. The interaction will take place in the order
        enemy interaction, key interaction, and exit interaction. Sends this info to game-manager to be handled."""

    def choose_name(self, name):
        """Set name inputted by player to the current player's name"""

    def update_info_from_game_manager(self, new_player):
        """Takes in an unpdated version of the player from the game-manager and sets the current player to these
        values"""
    


    def recieve_update(self, actor_update: RemoteActorUpdate):
        """Takes in the position and visible tiles,
        then updates the current player with that info (Also visually updates)"""
        msg = str(actor_update)
        self.__send(msg)


    def __send(self, msg):
        send_msg(self.socket, msg, self.name)

    def __receive(self):
        return receive_msg(self.socket, self.name)