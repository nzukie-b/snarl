from abc import ABC, abstractmethod

#TODO: Player abstract class
class Player(ABC):
    def __init__(self, name, loc, visible_tiles, current_player_health, inventory_contents):
        # Unique name chosen by the player
        self.name = name
        # Coordinate that shows location relative to the origin
        self.loc = loc
        # The visible tiles two grid coordinates away in cardinal or diagonal directions
        self.visible_tiles = visible_tiles
        self.current_player_health = current_player_health
        self.inventory_contents = inventory_contents

        def move_to_tile(self, move_location):
            """Move to a location within the visible tiles, if the same tile the player is currently on is
            selected as the move location then stay put as the move for that turn. Sends this info to game-manager to be
            handled."""

        def interact_with_tile_contents(self, current_tile_info):
            """Interact with the contents on the current tile if it exists. The interaction will take place in the order
            enemy interaction, key interaction, and exit interaction. Sends this info to game-manager to be handled."""

        def choose_name(self, name):
            """Set name inputted by player to the current player's name"""

        def update_info_from_game_manager(new_player):
            """Takes in an unpdated version of the player from the game-manager and sets the current player to these
            values"""

        def recieve_update(update):

