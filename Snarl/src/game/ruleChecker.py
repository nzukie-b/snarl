#!/usr/bin/env python
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/src'
sys.path.append(game_dir)
import random
from coord import Coord
from constants import A_WIN, EJECT, EXIT, GAME_END, GHOST, INFO, KEY, LEVEL_END, ORIGIN, P_WIN, ROOM, STATUS, TYPE, VALID_MOVE, ZOMBIE
from model.item import Item
from utilities import check_position, get_random_room_coord

class RuleChecker:
    def validate_player_movement(self, player, new_pos, level, players, adversaries):
        """Takes in old gamestate, level and new player state, then makes sure that new state is moving to a valid location
        location within the level and in relation to the other players/adversaries in the gamestate."""
        info = level.info_at_coord(new_pos)
        current_pos = player.pos
        valid_move = self.__vaildate_movement_distance(current_pos, new_pos, player.move_speed)
        # list of player coords with new pos filtered out
        other_coords = [coord for coord in players if coord != current_pos]
        # Invalid move if multiple coords are filtered out i.e. current_pos is shared by multiple adversaries
        if len(other_coords) > len(players) - 1:
            valid_move = False

        eject = False
        if valid_move:
            if new_pos in players:
                valid_move = False
            elif new_pos in adversaries:
                eject = True

        return {VALID_MOVE: valid_move, INFO: info, EJECT: eject}


    def validate_adversary_movement(self, adversary, new_adversary_pos, level, player_coords, adversary_coords):
        """Takes in old gamestate, level and new player state, then makes sure that new state is moving to a valid location
        location within the level and in relation to the other players/adversaries in the gamestate."""
        valid_move = None
        eject = False
        if adversary.type == ZOMBIE:
            valid_move = self.__validate_zombie_movement(adversary, new_adversary_pos, level, adversary_coords)
        elif adversary.type == GHOST:
            valid_move = self.__validate_ghost_movement(adversary, new_adversary_pos, level, adversary_coords)

        if new_adversary_pos in player_coords:
            eject = True
        
        return {VALID_MOVE: valid_move, EJECT: eject}

    def __valid_zombie_move(self, coord, walkable_tiles, adversary_coords, door_coords):
        '''Checks if the the provided coord is a valid tile for a zombie. That it is not the position of a door or other adversary'''
        return coord in walkable_tiles and (coord not in adversary_coords and coord not in door_coords)
        

    def __validate_zombie_movement(self, adversary, new_pos, level, adversary_coords):
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

            if self.__validate_movement_distance(adversary.pos, new_pos, adversary.move_speed):
                if self.__valid_zombie_move(new_pos, tiles, adversary_coords, door_coords):
                    return True
        else:
            return False
        
    def __validate_ghost_movement(self, adversary, new_pos, level, adversary_coords):
        valid_move = self.__validate_movement_distance(adversary.pos, new_pos, adversary.move_speed)
        if valid_move:
            move_info = level.info_at_coord(new_pos)
            if not move_info.traversable:
                # if new pos is not traversable such as being a wall move to a random room
                new_pos = get_random_room_coord(level)

            if new_pos in adversary_coords:
                valid_move = False
        
        return valid_move


    def __vaildate_movement_distance(self, current_pos, new_pos, move_distance):
        """Helper for validating movements, takes new players position compared to old player/adversary position and
        checks that the movement is within the cardinal distance relative to the player/adversary movement speed."""
        return 0 <= abs(current_pos.row - new_pos.row) + \
                   abs(current_pos.col - new_pos.col) <= move_distance


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




    def is_level_over(state):
        is_over = False
        status = None
        if len(state.out_players) == len(state.players):
            is_over = True
            if state.game_status == P_WIN:
                status = P_WIN
            else:
                status = A_WIN
        return {LEVEL_END: is_over, STATUS: status}

    def is_game_over(state):
        '''Checks whether the current state is one of the game end states. That is
        * - At least 1 player has exited the level, and all other players have been removed
        * - All players have been removed from the level by adversaries'''
        is_over = len(state.levels) == 0
        status = None
        if state.game_status == P_WIN:
             status = P_WIN
        else:
            status = A_WIN
        return {GAME_END: is_over, STATUS: status}

    

    def validate_item_interaction(self, player, item, state):
        """Checks that level items and player inventory have been properly updated after interaction between player
        and item. (In the case that adversaries can pick up items this would also check that interaction.)"""
        level = state.current_level
        for room in level.rooms:
            if item in room.items:
                return False

        if player.pos in level.exits and not state.exit_locked:
                state.ejected_players.add(player.name)
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