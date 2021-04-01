#!/usr/bin/env python
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/src'
sys.path.append(game_dir)
from coord import Coord
from constants import A_WIN, EXIT, GAME_END, INFO, KEY, ORIGIN, P_WIN, ROOM, STATUS, TYPE, VALID_MOVE, ZOMBIE
from model.item import Item
from utilities import check_position

class RuleChecker:
    def validate_player_movement(self, cur_player_loc, new_player_loc, level):
        """Takes in old gamestate, level and new player state, then makes sure that new state is moving to a valid location
        location within the level and in relation to the other players/adversaries in the gamestate."""

        info = level.info_at_coord(new_player_loc)


        return {VALID_MOVE: self.__vaildate_movement_distance(cur_player_loc, new_player_loc, True), INFO: info}


    def validate_adversary_movement(self, adversary, new_adversary_pos, level, player_coords, adversary_coords):
        """Takes in old gamestate, level and new player state, then makes sure that new state is moving to a valid location
        location within the level and in relation to the other players/adversaries in the gamestate."""
        if adversary.type == ZOMBIE:
            return self.__validate_zombie_movement(adversary, new_adversary_pos, level, player_coords, adversary_coords)


    def __valid_zombie_move(self, coord, walkable_tiles, adversary_coords, door_coords):
        '''Checks if the the provided coord is a valid tile for a zombie. That it is not the position of a door or other adversary'''
        return coord in walkable_tiles and (coord not in adversary_coords and coord not in door_coords)
        

    def __validate_zombie_movement(self, adversary, new_pos, level, player_coords, adversary_coords):
        '''Validates a moves according to the zombie movement rules. 
            * Only move 1 tile at a tile. Cannot skip moves, unless no other move is available. Cannot move onto a door. Cannot move onto adversaries'''
        cur_pos = adversary.pos
        rooms = [room for room in level.rooms]
        door_coords = [room.door for room in rooms]

        dest = check_position(new_pos, level)
        if dest[TYPE] == ROOM:
            origin = dest[ORIGIN]
            room = next(room for room in level.rooms if room.origin == origin)
            tiles = room.tiles
            if cur_pos == new_pos:
                up = Coord(cur_pos.row - 1, cur_pos.col)
                down = Coord(cur_pos.row + 1, cur_pos.col)
                left = Coord(cur_pos.row, cur_pos.col - 1)
                right = Coord(cur_pos.row, cur_pos.col + 1)


                if not self.__valid_zombie_move(up, tiles, adversary_coords, door_coords) and not self.__valid_zombie_move(
                    down, tiles, adversary_coords, door_coords) and not self.__valid_zombie_move(left, tiles, adversary_coords, door_coords) and not self.__valid_zombie_move(right, tiles, adversary_coords, door_coords):
                    return True
                else: return False

            if ((abs(cur_pos.row - new_pos.row) == 1) and cur_pos.col == new_pos.col) or (cur_pos.row == new_pos.row and (abs(cur_pos.col - new_pos.col) == 1)):
                if self.__valid_zombie_move(new_pos, tiles, adversary_coords, door_coords):
                    return True
        else:
            return False



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

