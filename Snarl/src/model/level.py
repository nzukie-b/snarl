#!/usr/bin/env python
import json
from utilities import check_dimensions, check_position, get_reachable_halls, get_reachable_rooms, to_point
from constants import EXIT, HALLWAY, KEY, ORIGIN, ROOM, TYPE

class CoordInfo:
    def __init__(self, traversable=None, obj='null', type_='void', reachable=None):
        self.traversable = traversable
        self.object = obj
        self.type = type_
        self.reachable = reachable if reachable else []

    def __str__(self):
        return '{{"traversable": {}, "object": {}, "type": {}, "reachable": {}}}'.format(self.traversable, self.object, self.type, self.reachable)

    def __repr__(self):
        return str(self)
class Level:
    def __init__(self, rooms, hallways, keys=None, exits=None):
        self.rooms = rooms
        self.hallways = hallways
        self.keys = keys if keys else []
        self.exits = exits if exits else []
    
    def __str__(self):
        rooms_str = [str(room) for room in self.rooms]
        halls_str = [str(hall) for hall in self.hallways]
        return json.dumps({"rooms": rooms_str, "hallways": halls_str})

    def __repr__(self):
        return str(self)

    def get_level_room_dimensions(self):
        '''Returns a set of ((row_origin, row_dest), (col_origin, col_dest)) representing the dimension boundaries of each room in the level'''
        room_dimensions = set()
        for room in self.rooms:
            row = (room.origin.row, room.origin.row + room.dimensions.row)
            col = (room.origin.col, room.origin.col + room.dimensions.col)
            old_room_size = len(room_dimensions)
            room_dimensions.add((row, col))
            # Element not added
            if old_room_size == len(room_dimensions):
                print('Invalid Level: Duplicate rooms')
                return None
        return room_dimensions

    def get_level_hallway_dimensions(self):
        '''Returns a set of ((row_origin, row_dest), (col_origin, col_dest)) representing the dimension boundaries of each hallway in the level'''
        hall_dimensions = set()
        for hall in self.hallways:
            row = (hall.origin.row, hall.origin.row + hall.dimensions.row)
            col = (hall.origin.col, hall.origin.col + hall.dimensions.col)
            old_hall_size = len(hall_dimensions)
            hall_dimensions.add((row, col)) 
            if old_hall_size == len(hall_dimensions):
                print('Invalid Level: Duplicate hallways')
                return None
        return hall_dimensions   

    #  Checks that there are not rooms/hallways sharing coordinates, or having overlapping dimensions
    def check_level_dimensions(self):
        '''Checks that this level has no rooms/hallways sharing coodinates or having overlapping dimensions'''
        room_dimensions = self.get_level_room_dimensions()
        hall_dimensions = self.get_level_hallway_dimensions()
        if not (hall_dimensions and room_dimensions):
            return False
        level_size = len(room_dimensions) + len(hall_dimensions)
        level_dimensions = room_dimensions.union(hall_dimensions)
        if level_size != len(level_dimensions):
            print('Invalid Level: Hallway or Room sharing coordinates')
            return False
        for coord in level_dimensions:
            # Remove the coordinate used for comparison from the set to avoid counting itself.
            updated_lvl_dimensions = [level for level in level_dimensions if level != coord]
            if check_dimensions(coord[0], coord[1], updated_lvl_dimensions):
                print('Invalid Level: Overlapping Room(s) or Hallway(s)')
                return False
        return True

    def info_at_coord(self, coord):
        '''Checks if the tile at the provided coordinate is within the bounds of the level. If so, it will return and object with the following info
            - whether the tile is traversable : .traversable
            - whether the tile it references contains a key or an exit : .object
            - if it is a hallway, or room : .type
            - if a hallway the origins of the connecting rooms | if a room the origins of neighboring rooms, that is, the rooms that are one hallway removed from the current room : .reachable'''
        
        result = CoordInfo()

        pos_info = check_position(coord, self)
        is_room = pos_info[TYPE] == ROOM
        origin = pos_info[ORIGIN]
        if not origin:
            result.traversable = False
        else: 
            if is_room == True:
                for room in self.rooms:
                    if origin == room.origin:
                        result.type = ROOM
                        result.traversable = coord in room.tiles
                    reachable = get_reachable_rooms(origin, self)
                    reachable = [] if reachable is None else reachable
                    result.reachable = [to_point(coord) for coord in reachable]

            elif is_room == False:
                for hall in self.hallways:
                    if origin == hall.origin:
                        result.type = HALLWAY
                        traversable = coord.row in range(hall.origin.row, hall.origin.row + hall.dimensions.row + 1) and coord.col in range(hall.origin.col, hall.origin.col + hall.dimensions.col + 1)
                        result.traversable = traversable
                    reachable = get_reachable_halls(origin, self)
                    reachable = [] if reachable is None else reachable
                    result.reachable = [to_point(coord) for coord in reachable]
                        
            if coord in self.exits:
                result.object = EXIT
            if coord in self.keys:
                result.object = KEY
        return result
