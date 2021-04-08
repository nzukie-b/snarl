import sys, os, random

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from coord import Coord
from common.adversary import Adversary
# from utilities import to_coord
from constants import G_RNG, HALLWAY, ORIGIN, ROOM, TYPE, ZOMBIE, GHOST, Z_RNG
from utilities import check_position, get_cardinal_coords, get_closest_coord

class RemoteAdversary(Adversary):
    def __init__(self, name, type_=ZOMBIE, adversary_obj=None, current_level=None, player_coords=None, adversary_coords=None):
        super().__init__(name=name, type_=type_, adversary_obj=adversary_obj, current_level=current_level,
         player_coords=player_coords, adversary_coords=adversary_coords)