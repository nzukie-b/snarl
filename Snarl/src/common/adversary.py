import sys, os, random
from abc import ABC, abstractmethod
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from constants import G_RNG, HALLWAY, ORIGIN, ROOM, TYPE, ZOMBIE, GHOST, Z_RNG
from coord import Coord
from utilities import get_cardinal_coords, check_position, get_closest_coord
from game.ruleChecker import RuleChecker

class Adversary(ABC):
    def __init__(self, name, type_=ZOMBIE, adversary_obj=None, current_level=None, player_coords=None, adversary_coords=None):
        self.name = name
        self.type = type_
        self.adversary_obj = adversary_obj
        self.current_level = current_level
        self.player_coords = player_coords
        self.adversary_coords = adversary_coords

    @abstractmethod
    def update_current_level(self, new_level):
        self.current_level = new_level
        # TODO: Update adversary pos with new level here or in start game?
        self.adversary_obj.pos = None
    
    @abstractmethod
    def update_player_coords(self, new_coords):
        self.player_coords = new_coords

    @abstractmethod
    def move_to_tile(self, gm):
        cur_pos = self.adversary_obj.pos
        move = self.__move_to_player(cur_pos)
        # Player noticed in range. returned a coordinate
        possible_moves = get_cardinal_coords(cur_pos)
        pos_info = check_position(cur_pos, self.current_level)
        if move is None:
            if self.type == ZOMBIE:
                move = self.__move_ghost(cur_pos, pos_info, possible_moves)
            elif self.type == GHOST:
                move = self.__move_ghost(cur_pos, pos_info, possible_moves)

        if move == None or move == 'null': move = self.adversary_obj.pos
        move_info = gm.request_adversary_move(self.name, move)
        if move_info is not None:
            self.adversary_obj = gm.get_adversary_actor(self.name)
        else:
            print('Invalid adversary move')
            return False

    def __player_noticed(self, cur_pos, coord, distance):
        return RuleChecker.validate_movement_distance(cur_pos, coord, distance)

    def __move_to_player(self, cur_pos) -> Coord:
        '''If a player is in notice range, returns a coord one tile closer to the player. Else None'''
        move = None
        if self.type == ZOMBIE:
            for coord in self.player_coords:
                if self.__player_noticed(cur_pos, coord, Z_RNG):
                    move = get_closest_coord(cur_pos, coord)
        elif self.type == GHOST:
            for coord in self.player_coords:
                if self.__player_noticed(cur_pos, coord, G_RNG):
                    move = get_closest_coord(cur_pos, coord)
        return move
    
    def __move_ghost(self, cur_pos, pos_info, possible_moves) -> Coord:
        move = None
        if pos_info[TYPE] == ROOM:
            for room in self.current_level.rooms:
                if room.origin == pos_info[ORIGIN]:
                    # If any of the possible moves 
                    valid_moves = list(set(possible_moves) - set(room.tiles))
                    if valid_moves:
                        move = random.choice(valid_moves)
        elif pos_info[TYPE] == HALLWAY:
            for hall in self.current_level.hallways:
                if hall.origin == pos_info[ORIGIN]:
                    row_start = hall.origin.row
                    row_end = hall.origin.row + hall.dimensions.row
                    col_start = hall.origin.col
                    col_end = hall.origin.col + hall.dimensions.col
                    valid_moves = [m for m in possible_moves if m.row not in range(row_start, row_end + 1) or m.col not in range(col_start, col_end)]
                    if not valid_moves:
                        door1 = get_closest_coord(cur_pos, hall.doors[0])
                        door2 = get_closest_coord(cur_pos, hall.doors[1])
                        valid_moves = [door1, door2]
                    move = random.choice(valid_moves)
        return move

    def __move_zombie(self, cur_pos, pos_info, possible_moves) -> Coord:
        move = None
        if pos_info[TYPE] == ROOM:
            room_origin = pos_info[ORIGIN]
            for room in self.current_level.rooms:
                if room.origin == room_origin:
                    # Valid tiles in the room do not include doors
                    valid_moves = list(set(possible_moves) & set(room.tiles) - set(room.doors))
                    if valid_moves:
                        move = random.choice(valid_moves)
        return move