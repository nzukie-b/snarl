import sys, os, random

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from coord import Coord
from common.adversary import Adversary
# from utilities import to_coord
from constants import G_RNG, HALLWAY, ORIGIN, ROOM, TYPE, ZOMBIE, GHOST, Z_RNG
from utilities import check_position, get_cardinal_coords, get_closest_coord

class LocalAdversary(Adversary):
    def __init__(self, name, type_=ZOMBIE, adversary_obj=None, current_level=None, player_coords=None, adversary_coords=None):
        super().__init__(name=name, type_=type_, adversary_obj=adversary_obj, current_level=current_level,
         player_coords=player_coords, adversary_coords=adversary_coords)

    def move_to_tile(self, move, gm):
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
        return super().move_to_tile(move, gm)

    def __player_noticed(self, cur_pos, coord, distance):
        return self.rc.validate_movement_distance(cur_pos, coord, distance)


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

    def update_current_level(self, new_level):
        return super().update_current_level(new_level)

    def update_player_coords(self, new_coords):
        return super().update_player_coords(new_coords)
        