#!/usr/bin/env python
import json
from coord import Coord
from room import Room
from constants import SIZE, HEIGTH, WIDTH

def check_hallway(hallway):
    '''Checks that a hallway is valid by checking that the hallway's orientation is either vertical or horizontal.'''
    try:
        hallway.check_orientation()
        return True
    except Exception as err:
        print(err)
        return False


# Since valid_doors is only checked after valid_tiles is True it is not an issue that check_doors does not guarantee that the walkable tiles are inside the room as check_tiles handles guarantees that 
def check_room(room):
    '''Checks that the provided room is valid by checking the tiles and doors of the provided room'''
    valid_tiles = room.check_tiles()
    valid_doors = room.check_doors()
    if not valid_tiles:
        print('Invalid Room: Walkable tile(s) outside of room dimensions')
        return False
    if not valid_doors:
        print('Invalid Room: Door(s) outside of walkable tiles')
        return False
    return True


# Checks that the provided coordinates are not within the provided coordinates. True if the provided coordinates do not both fall the level dimensions
def check_dimensions(x_dimensions, y_dimensions, level_dimensions):
    '''Checks that the provided coordinates, are within the level dimensions. 
        If so, returns the origin of the room/hallway overlapping the point. If the provided coordinates are not within the level returns None'''
    x_start = x_dimensions[0]
    x_end = x_dimensions[1]
    y_start = y_dimensions[0]
    y_end = y_dimensions[1]
    for level in level_dimensions:
        # level is tuple in format ((x_origin, x_origin+dest), (y_origin, y_origin+dest)), Created in check_level_dimensions
        level_x_origin = level[0][0]
        level_x_dest = level[0][1]
        level_y_origin = level[1][0]
        level_y_dest = level[1][1]
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end +1):
                if x in range(level_x_origin, level_x_dest + 1) and y in range(level_y_origin, level_y_dest + 1):
                    return Coord(level_x_origin, level_y_origin)
        return None

def check_level(level):
    '''Checks that the provided level is valid'''
    for room in level.rooms:
        if check_room(room) == False:
            return False
    for hall in level.hallways:
        try:
            check_hallway(hall)
        except Exception as err:
            return False
    return level.check_level_dimensions()

def parse_room(room_input):
    room_json = json.loads(room_input)
    if room_json[0]['type'] != 'room':
        print(room_json['type'])
        print('Invalid Args: Type is not room')
        return False
    origin = room_json[0]['origin']
    bounds = room_json[0]['bounds']
    layout = room_json[0]['layout']
    point = room_json[1]
    origin_coord = Coord(origin[0], origin[1])
    dimensions = Coord(bounds['rows'], bounds['columns'])
    tiles = []
    doors = []
    for ii in range(0, bounds['rows']):
        for jj in range(0, bounds['columns']):
            # ii = x jj = y
            if layout[ii][jj] != 0:
                tiles.append(Coord(origin[0] + ii, origin[1] + jj))
            if layout[ii][jj] == 2:
                doors.append(Coord(origin[0] + ii, origin[1] + jj))
    room_obj = Room(origin_coord, dimensions, tiles, doors)
    if (point[0] not in range(origin_coord.x, origin_coord.x + dimensions.x + 1)) or (point[1] not in range(origin_coord.y, origin_coord.y + dimensions.y + 1)):
        print('[ Failure: Point ", {} , " is not in room at ", {} ]'.format(point, origin))
        return False
    reachable_coords = room_obj.get_reachable_tiles(Coord(point[0], point[1]))
    reachable_tiles = []
    for coord in reachable_coords:
        reachable_tiles.append([coord.x, coord.y])
    print('[ Success: Traversable points from, " {} ," in room at ", {}, " are ", {} ]'.format(point, origin, reachable_tiles))
    return reachable_tiles
