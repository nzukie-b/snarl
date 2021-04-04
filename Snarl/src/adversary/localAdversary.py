import sys, os

from constants import ZOMBIE
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from common.adversary import Adversary
from game.ruleChecker import RuleChecker
from utilities import to_coord
from constant import ZOMBIE, GHOST

class LocalAdversary(Adversary):
    def __init__(self, name, type_=ZOMBIE, adversary_obj=None, current_level=None, player_coords=None, adversary_coords=None):
        super().__init__(name=name, type_=type_, adversary_obj=adversary_obj, current_level=current_level,
         player_coords=player_coords, adversary_coords=adversary_coords)

    def move_to_tile(self, move, gm):
        if self.type_ == ZOMBIE:
            self.move_zombie()

        if self.type_ == GHOST:
            self.move_ghost()

        return super().move_to_tile(move, gm)

    def move_zombie(self):
        for pc in self.player_coords:
            pc_new = pc + to_coord([1, 1])
            # Zombie can see the same distance as the player, checks around radius to see if player is within range.
            RuleChecker.__vaildate_movement_distance(pc, pc_new, 5)

        RuleChecker.__validate_zombie_movement()

    def move_ghost(self):
        for pc in self.player_coords:
            pc_new = pc + to_coord([1, 1])
            # Ghost can see twice the distance, checks around the larger radius to see if player is within range.
            RuleChecker.__vaildate_movement_distance(pc, pc_new, 9)

        RuleChecker.__validate_ghost_movement()


    def update_current_level(self, new_level):
        return super().update_current_level(new_level)

    def update_player_coords(self, new_coords):
        return super().update_player_coords(new_coords)
        