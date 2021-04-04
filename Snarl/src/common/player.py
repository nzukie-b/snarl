from abc import ABC, abstractmethod
class Player(ABC):
    def __init__(self, name, player_obj=None, layout=None, visible_tiles=None, actors=None, objects=None, inventory_contents=None):
        # Unique name chosen by the player
        self.name = name
        #playerActor
        self.player_obj = player_obj
        # Coordinate that shows location relative to the origin
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
        if move == None or  move == 'null': move = self.player_obj.pos
        move_info = gm.request_player_move(self.name, move)
        if move_info:
            self.player_obj = gm.get_player_actor(self.name)
        else:
            #Player is trying to go twice or invalid player name
            print("Invalid Player")
        return None



    @abstractmethod
    def interact_with_tile_contents(self, current_tile_info):
        """Interact with the contents on the current tile if it exists. The interaction will take place in the order
        enemy interaction, key interaction, and exit interaction. Sends this info to game-manager to be handled."""

    @abstractmethod
    def choose_name(self, name):
        """Set name inputted by player to the current player's name"""

    @abstractmethod
    def update_info_from_game_manager(self, new_player):
        """Takes in an unpdated version of the player from the game-manager and sets the current player to these
        values"""

    @abstractmethod
    def recieve_update(self, actor_update):
        """Takes in the position and visible tiles,
        then updates the current player with that info (Also visually updates)"""
        self.player_obj.pos = actor_update.position
        self.visible_tiles = actor_update.layout_coords
        self.layout = actor_update.layout
        self.actors = actor_update.actors
        self.objects = actor_update.objects

