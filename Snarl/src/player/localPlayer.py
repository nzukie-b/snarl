import sys, os
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from common.player import Player


# TODO Implementation of common.player
class Player(Player):
    def __init__(self, name, loc, visible_tiles, current_player_health, inventory_contents):
        super().__init__()

        def move_to_tile(self, move, gm):
            """Move to a location within the visible tiles, if the same tile the player is currently on is
            selected as the move location then stay put as the move for that turn. Sends this info to game-manager to be
            handled."""
            super().move_to_tile()

        def interact_with_tile_contents(self, current_tile_info):
            """Interact with the contents on the current tile if it exists. The interaction will take place in the order
            enemy interaction, key interaction, and exit interaction. Sends this info to game-manager to be handled."""

        def choose_name(self, name):
            """Set name inputted by player to the current player's name"""

        def update_info_from_game_manager(new_player):
            """Takes in an unpdated version of the player from the game-manager and sets the current player to these
            values"""

        def recieve_update(actor_update):
            """Takes in the position and visible tiles,
            then updates the current player with that info (Also visually updates)"""
            super().recieve_updaate(actor_update)
            print(self.layout)