from abc import ABC, abstractmethod
import game.gameManager
#TODO: Player abstract class
class Player(ABC):
    def __init__(self, name, loc=None, layout=None, visible_tiles=None, actors=None, objects=None, inventory_contents=None):
        # Unique name chosen by the player
        self.name = name
        # Coordinate that shows location relative to the origin
        self.pos = loc
        self.layout = layout
        # The visible tiles two grid coordinates away in cardinal or diagonal directions
        self.visible_tiles = visible_tiles
        self.actors = actors
        self.objects = objects
        self.visible_tiles = visible_tiles
        self.inventory_contents = inventory_contents

        @abstractmethod
        def move_to_tile(self, move, gm):
            """Move to a location within the visible tiles, if the same tile the player is currently on is
            selected as the move location then stay put as the move for that turn. Sends this info to game-manager to be
            handled."""
            if move == None or  move == 'null': move = self.pos
            move_info = gm.request_player_move(name, move)
            if move_info is not None:
                self.pos = next(player.pos for player in gm.players)
            else:
                print("Invalid Player")
            
            

        @abstractmethod
        def interact_with_tile_contents(self, current_tile_info):
            """Interact with the contents on the current tile if it exists. The interaction will take place in the order
            enemy interaction, key interaction, and exit interaction. Sends this info to game-manager to be handled."""

        @abstractmethod
        def choose_name(self, name):
            """Set name inputted by player to the current player's name"""

        @abstractmethod
        def update_info_from_game_manager(new_player):
            """Takes in an unpdated version of the player from the game-manager and sets the current player to these
            values"""

        @abstractmethod
        def recieve_update(actor_update):
            """Takes in the position and visible tiles,
            then updates the current player with that info (Also visually updates)"""
            self.pos = actor_update.pos
            self.visible_tiles = actor_update.layout_coords
            self.actors = actor_update.actors
            self.objects = actor_update.objects

