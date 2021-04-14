import sys, os
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from common.player import Player
from remote.messages import RemoteActorUpdate
from utilities import to_coord
from view.view import render_player_view
class LocalPlayer(Player):
    def __init__(self, name, player_obj=None, layout=None, visible_tiles=None, actors=None, objects=None, inventory_contents=None):
        super().__init__(name=name, player_obj=player_obj, layout=layout, visible_tiles=visible_tiles, 
        actors=actors, objects=objects, inventory=inventory_contents)

    def move_to_tile(self, gm):
        """Move to a location within the visible tiles, if the same tile the player is currently on is
        selected as the move location then stay put as the move for that turn. Sends this info to game-manager to be
        handled."""
        move = input("Please provide a move of the format 'row, col': ")
        move = to_coord(move)
        super().move_to_tile(move, gm)

    def interact_with_tile_contents(self, current_tile_info):
        """Interact with the contents on the current tile if it exists. The interaction will take place in the order
        enemy interaction, key interaction, and exit interaction. Sends this info to game-manager to be handled."""

    def choose_name(self, name):
        """Set name inputted by player to the current player's name"""

    def update_info_from_game_manager(self, new_player):
        """Takes in an unpdated version of the player from the game-manager and sets the current player to these
        values"""

    def recieve_update(self, actor_update):
        """Takes in the position and visible tiles,
        then updates the current player with that info (Also visually updates)"""
        super().recieve_update(actor_update)
        layout_actors = self.actors
        layout_objects = self.objects
        self.layout = str(self.layout).replace('[[', '[').replace('], ', ']\n').replace(']]', ']\n')
        # print(self.layout)
        print(self.layout + 'Position: {}\nActors Visible: {}\nObjects Visible: {}'.format(actor_update.position, layout_actors, layout_objects))
        if isinstance(actor_update, RemoteActorUpdate):
            print(actor_update.message)