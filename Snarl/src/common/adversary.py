from abc import ABC, abstractmethod
from constants import GHOST, ZOMBIE

class Adversary(ABC):
    def __init__(self, name, type_=ZOMBIE, adversary_obj=None, current_level=None, player_coords=None, adversary_coords=None):
        self.name = name
        self.type = type_
        self.adversary_obj = adversary_obj
        self.current_level = current_level
        self.player_coords = player_coords
        self.adversary_coords = adversary_coords

    @abstractmethod
    def update_current_level(self, new_level):
        self.current_level = new_level
        # TODO: Update adversary pos with new level here or in start game?
        self.adversary_obj.pos = None
    
    @abstractmethod
    def update_player_coords(self, new_coords):
        self.player_coords = new_coords

    @abstractmethod
    def move_to_tile(self, move, gm):
        if move == None or move == 'null': move = self.adversary_obj.pos
        move_info = gm.request_adversary_move(self.name, move)
        if move_info is not None:
            self.adversary_obj = gm.get_adversary_actor(self.name)
        else:
            print('Invalid adversary move')
            return False

