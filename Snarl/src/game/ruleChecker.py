#!/usr/bin/env python
import sys, os
from typing import List


currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/src'
sys.path.append(game_dir)
from coord import Coord
from model.actor import Actor
from model.player import PlayerActor
from model.adversary import AdversaryActor
from model.gamestate import GameState
from constants import A_WIN, EJECT, EXIT, GAME_END, GHOST, INFO, KEY, LEVEL_END, OK, ORIGIN, P_WIN, ROOM, STATUS, TYPE, VALID_MOVE, ZOMBIE
from model.item import Item
from model.level import Level
from utilities import check_position, get_cardinal_coords, get_random_room_coord

class RuleChecker:

    @staticmethod
    def validate_movement_distance(current_pos, new_pos, move_distance) -> bool:
        """Helper for validating movements, takes new players position compared to old player/adversary position and
        checks that the movement is within the cardinal distance relative to the player/adversary movement speed."""
        return 0 <= abs(current_pos.row - new_pos.row) + \
                   abs(current_pos.col - new_pos.col) <= move_distance

    def __validate_attack(self, attacker: Actor, targets: List[Actor], new_pos: Coord):
        """Validates attack interaction between the two types of Actors"""
        for target in targets:
            if new_pos == target.pos:
                print('ATTACKER: ', attacker.name, 'HEALTH: ', attacker.health)
                print('TARGET ', target.name, 'HEALTH: ',target.health)
                target.health = target.health - attacker.atk_power
                if target.health <= 0:
                    print('KILLED: ', target.name, 'HEALTH: ', target.health)
                    return target.name


    def validate_player_movement(self, player: PlayerActor, new_pos: Coord, level: Level, player_coords: List[Coord], adversaries: List[AdversaryActor]):
        """Takes in old gamestate, level and new player state, then makes sure that new state is moving to a valid location
        location within the level and in relation to the other players/adversaries in the gamestate."""
        info = level.info_at_coord(new_pos)
        current_pos = player.pos
        valid_move = self.validate_movement_distance(current_pos, new_pos, player.move_speed)
        # list of player coords with new pos filtered out
        eject = None
        if valid_move:
            if new_pos in player_coords:
                valid_move = False
            eject = self.__validate_attack(player, adversaries, new_pos)

        return {VALID_MOVE: valid_move, INFO: info, EJECT: eject}


    def validate_adversary_movement(self, adversary: AdversaryActor, new_pos: Coord, level: Level, players: List[PlayerActor], adversary_coords: List[Coord]):
        """Takes in old gamestate, level and new player state, then makes sure that new state is moving to a valid location
        location within the level and in relation to the other players/adversaries in the gamestate."""
        valid_move = None
        eject = False
        if adversary.type == ZOMBIE:
            valid_move = self.__validate_zombie_movement(adversary, new_pos, level, adversary_coords)
        elif adversary.type == GHOST:
            valid_move = self.__validate_ghost_movement(adversary, new_pos, level, adversary_coords)
        if valid_move:
            eject = self.__validate_attack(adversary, players, new_pos)
        
        return {VALID_MOVE: valid_move, EJECT: eject}

    def __valid_adversary_pos(self, coord, walkable_tiles, adversary_coords, door_coords):
        '''Checks if the the provided coord is a valid tile for a zombie. That it is not the position of a door or other adversary'''
        return coord in walkable_tiles and (coord not in adversary_coords and coord not in door_coords)
        

    def __validate_zombie_movement(self, adversary: AdversaryActor, new_pos, level, adversary_coords):
        '''Validates a moves according to the zombie movement rules. 
            * Only move 1 tile at a tile. Cannot skip moves, unless no other move is available. Cannot move onto a door. Cannot move onto adversaries'''
        cur_pos = adversary.pos
        rooms = [room for room in level.rooms]
        door_coords = [room.doors for room in rooms]

        dest = check_position(new_pos, level)
        if dest[TYPE] == ROOM:
            origin = dest[ORIGIN]
            room = next(room for room in level.rooms if room.origin == origin)
            tiles = room.tiles
            if cur_pos == new_pos:
                directions = get_cardinal_coords(cur_pos)
                
                for d in directions:
                    if not self.__valid_adversary_pos(d, tiles, adversary_coords, door_coords):
                        return True
                        
            if self.validate_movement_distance(cur_pos, new_pos, adversary.move_speed):
                if self.__valid_adversary_pos(new_pos, tiles, adversary_coords, door_coords):
                    return True
        else:
            return False
        
    def __validate_ghost_movement(self, adversary, new_pos, level, adversary_coords) -> bool:
        valid_move = self.validate_movement_distance(adversary.pos, new_pos, adversary.move_speed)
        # print('VALID', valid_move)
        # print('POSINFO:', pos_info)
        if not valid_move:
            # ghost was teleported
            valid_move = True
        if valid_move:
            if new_pos in adversary_coords:
                valid_move = False
        
        return valid_move

    def validate_interaction(self, gamestate, player_or_adversary, player_or_adversary1):
        """Checks validity of interaction between two players/adversaries, interaction is automatically invalid if it
        it between two players."""


    def __players_eliminated(self, state: GameState):
        player_names = [p.name for p in state.players]
        for name in player_names:
            if name not in state.out_actors:
                return False
        return True


    def is_level_over(self, state):
        is_over = False
        status = None
        if self.__players_eliminated(state):
            is_over = True
            if state.game_status == P_WIN:
                status = P_WIN
            else:
                status = A_WIN
        return {LEVEL_END: is_over, STATUS: status}

    def is_game_over(self, start_level, next_level, state):
        '''Checks whether the current state is one of the game end states. That is
        * - At least 1 player has exited the level, and all other players have been removed
        * - All players have been removed from the level by adversaries'''
        level_over = self.is_level_over(state)
        is_over = (level_over[LEVEL_END] and start_level == next_level) or (level_over[LEVEL_END] and level_over[STATUS] == A_WIN)
        status = None
        if state.game_status == P_WIN:
             status = P_WIN
        else:
            status = A_WIN
        return {GAME_END: is_over, STATUS: status}

    

    def validate_item_interaction(self, player, item_pos, state):
        """Checks that level items and player inventory have been properly updated after interaction between player
        and item. (In the case that adversaries can pick up items this would also check that interaction.)"""
        level = state.current_level
        for room in level.rooms:
            room_items = [item.pos for item in room.items]
            try:
                item = next(item for item in room.items if item.pos == item_pos)
                if item_pos in room_items:
                    return False
            except StopIteration:
                pass
                # No should be found as it should have been removed from the room
            try:
                item = next(item for item in player.inventory if item.pos == item_pos)
            except StopIteration:
                # If there is no item with the current pos in the player's inventory, then this is an invalid interaction
                return False

        res = OK
        inventory = [item.pos for item in player.inventory]
        if player.pos in level.exits and not state.exit_locked:
                state.out_players.append(player.name)
                state.game_status == P_WIN
                res = EXIT
                # game_info = self.is_game_over(state)
                # TODO: What to actually do once game is over?
                # if game_info[GAME_END]:
        elif item_pos in inventory:
            if isinstance(item, Item):
                if item.type == KEY and state.exit_locked:
                    state.exit_locked = False
                res = KEY
        return res