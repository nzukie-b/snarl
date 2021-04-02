import sys, os

from constants import ZOMBIE
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from common.adversary import Adversary

class LocalAdversary(Adversary):
    def __init__(self, name, type_=ZOMBIE, adversary_obj=None, current_level=None, player_coords=None, adversary_coords=None):
        super().__init__(name=name, type_=type_, adversary_obj=adversary_obj, current_level=current_level,
         player_coords=player_coords, adversary_coords=adversary_coords)

    def move_to_tile(self, move, gm):
        return super().move_to_tile(move, gm)

    def update_current_level(self, new_level):
        return super().update_current_level(new_level)

    def update_player_coords(self, new_coords):
        return super().update_player_coords(new_coords)
        