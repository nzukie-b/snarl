import sys, os

from constants import ZOMBIE
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from common.adversary import Adversary
# from utilities import to_coord
from constants import ZOMBIE, GHOST

class LocalAdversary(Adversary):
    def __init__(self, name, type_=ZOMBIE, adversary_obj=None, current_level=None, player_coords=None, adversary_coords=None):
        super().__init__(name=name, type_=type_, adversary_obj=adversary_obj, current_level=current_level,
         player_coords=player_coords, adversary_coords=adversary_coords)

    def move_to_tile(self, move, gm):
        # Abstract class move calls rulechecker. No validation needed here
        return super().move_to_tile(move, gm)

# TODO: Sort out circular imports for this section
    # def move_zombie(self):
        # for pc in self.player_coords:
            # pc_new = pc + to_coord([1, 1])
            # Zombie can see the same distance as the player, checks around radius to see if player is within range.
            # self.rc.__vaildate_movement_distance(pc, pc_new, 5)

        # self.rc.__validate_zombie_movement()

    # def move_ghost(self):
        # for pc in self.player_coords:
            # pc_new = pc + to_coord([1, 1])
            # Ghost can see twice the distance, checks around the larger radius to see if player is within range.
            # self.rc.__vaildate_movement_distance(pc, pc_new, 9)

        # self.rc.__validate_ghost_movement()


    def update_current_level(self, new_level):
        return super().update_current_level(new_level)

    def update_player_coords(self, new_coords):
        return super().update_player_coords(new_coords)
        