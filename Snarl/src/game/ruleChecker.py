#!/usr/bin/env python
import sys, os
import pytest

currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/src'
sys.path.append(game_dir)
from coord import Coord

class RuleChecker:
    def validate_player_movement(self, cur_player_loc, new_player_loc, level):
        """Takes in old gamestate, level and new player state, then makes sure that new state is moving to a valid location
        location within the level and in relation to the other players/adversaries in the gamestate."""

        info = level.info_at_coord(new_player_loc)

        return True and self.__vaildate_movement_distance(cur_player_loc, new_player_loc, True) and info.traversable


    def validate_adversary_movement(self, gamestate, level, new_adversary):
        """Takes in old gamestate, level and new player state, then makes sure that new state is moving to a valid location
        location within the level and in relation to the other players/adversaries in the gamestate."""


    def __vaildate_movement_distance(self, new_player_or_adversary_pos, old_player_or_adversary_pos, is_player):
        """Helper for validating movements, takes new players position compared to old player/adversary position and
        checks that the movement is within the cardinal distance relative to the player/adversary movement speed."""
        if is_player:
            return 0 <= abs(new_player_or_adversary_pos.row - old_player_or_adversary_pos.row) + \
                   abs(new_player_or_adversary_pos.col - old_player_or_adversary_pos.col) <= 2


    def validate_interaction(self, gamestate, player_or_adversary, player_or_adversary1):
        """Checks validity of interaction between two players/adversaries, interaction is automatically invalid if it
        it between two players."""


    def validate_player_attack(self, gamestate, player, adversary):
        """Helper for interaction validation that checks if the attack from the player to the adversary does
        the proper amount of damage. Also checks that adversary is removed from gamestate if they are killed
        by the attack."""


    def validate_adversary_attack(self, gamestate, player, adversary):
        """helper for interaction validation that checks if the attack from the adversary to the player does the
        proper amount of damage. Also checks that adversary is removed from gamestate if they are killed
        by the attack."""


    def validate_item_interaction(self, player, item, level):
        """Checks that level items and player inventory have been properly updated after interaction between player
        and item. (In the case that adversaries can pick up items this would also check that interaction.)"""
        for room in level.rooms:
            print(str(room))
            if item in room.items:
                return False

        for pi in player.inventory:
            if item == Coord(pi.row, pi.col):
                return False

        return True
