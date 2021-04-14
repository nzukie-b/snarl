import sys, os, random

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from coord import Coord
from common.adversary import Adversary
# from utilities import to_coord
from constants import G_RNG, HALLWAY, ORIGIN, ROOM, TYPE, ZOMBIE, GHOST, Z_RNG

class RemoteAdversary(Adversary):
    def __init__(self, name, type_, adversary_obj, current_level, player_coords, adversary_coords):
        super().__init__(name=name, type_=type_, adversary_obj=adversary_obj, current_level=current_level,
         player_coords=player_coords, adversary_coords=adversary_coords)

    def move_to_tile(self, gm):
        return super().move_to_tile(gm)

    def update_current_level(self, new_level):
        return super().update_current_level(new_level)

    def update_player_coords(self, new_coords):
        return super().update_player_coords(new_coords)

