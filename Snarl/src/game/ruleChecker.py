#!/usr/bin/env python
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/src'
sys.path.append(game_dir)
from coord import Coord
from constants import A_WIN, EXIT, GAME_END, INFO, KEY, P_WIN, STATUS, VALID_MOVE
from model.item import Item

class RuleChecker:
    def validate_player_movement(self, cur_player_loc, new_player_loc, level):
        """Takes in old gamestate, level and new player state, then makes sure that new state is moving to a valid location
        location within the level and in relation to the other players/adversaries in the gamestate."""

        info = level.info_at_coord(new_player_loc)


        return {VALID_MOVE: self.__vaildate_movement_distance(cur_player_loc, new_player_loc, True), INFO: info}


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



    def is_game_over(state):
        '''Checks whether the current state is one of the game end states. That is
        * - At least 1 player has exited the level, and all other players have been removed
        * - All players have been removed from the level by adversaries'''
        is_over = False
        status = None
        if len(state.out_players) == len(state.players):
            is_over = True
            if state.game_status == P_WIN:
                status = P_WIN
            else:
                status = A_WIN
        return {GAME_END: is_over, STATUS: status}

    

    def validate_item_interaction(self, player, item, state):
        """Checks that level items and player inventory have been properly updated after interaction between player
        and item. (In the case that adversaries can pick up items this would also check that interaction.)"""
        level = state.level
        for room in level.rooms:
            if item in room.items:
                return False

        if player.pos in level.exits and not state.exit_locked:
                state.out_players.add(player)
                state.game_status == P_WIN
                return True
                # game_info = self.is_game_over(state)
                # TODO: What to actually do once game is over?
                # if game_info[GAME_END]:
        elif item in player.inventory:
            if isinstance(item, Item):
                if item.type == KEY and state.exit_locked:
                    state.exit_locked = False
        return True

        return False

