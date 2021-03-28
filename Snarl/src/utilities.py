#!/usr/bin/env python
from common.player import Player
from coord import Coord
from constants import HALLWAY, ROOM
from player.localPlayer import LocalPlayer
from model.player import PlayerActor

def check_hallway(hallway):
    '''Checks that a hallway is valid by checking that the hallway's orientation is either vertical or horizontal.'''
    try:
        hallway.check_orientation()
        return True
    except Exception as err:
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
    row_start = x_dimensions[0]
    row_end = x_dimensions[1]
    col_start = y_dimensions[0]
    col_end = y_dimensions[1]
    for level in level_dimensions:
        # level_dimensions list of tuples in format ((x_origin, x_origin+dest), (y_origin, y_origin+dest)), Created in check_level_dimensions
        level_row_origin = level[0][0]
        level_row_dest = level[0][1]
        level_col_origin = level[1][0]
        level_col_dest = level[1][1]
        for row in range(row_start, row_end + 1):
            for col in range(col_start, col_end + 1):
                # print(x,y)
                if row in range(level_row_origin, level_row_dest + 1) and col in range(level_col_origin, level_col_dest + 1):
                    return Coord(level_row_origin, level_col_origin)
    return None

def check_level(level):
    '''Checks that the provided level is valid'''
    for room in level.rooms:
        if check_room(room) == False:
            #print("ROOM CHECK FAILED")
            return False
    for hall in level.hallways:
            if check_hallway(hall) == False:
                return False
    #print("dimension check: " + str(level.check_level_dimensions()))
    return level.check_level_dimensions()

def get_reachable_tiles(coord, walkable_tiles):
    '''Takes in a list of walkable tiles, and returns a list of tiles reachable within a 1 space move'''
    tiles = []
    for tile in walkable_tiles:
        #TODO: Separate this into some coord comparison function?
        if (tile.row == coord.row) and (tile.col ==  coord.col + 1 or tile.col == coord.col - 1):
            tiles.append(tile)
        elif (tile.col == coord.col) and (tile.row == coord.row + 1 or tile.row == coord.row - 1):
            tiles.append(tile)
    return tiles


def to_coord(point):
    '''Converts the point coordinate system i.e. [0, 0] to a Coord object {row: 0, col:0}'''
    if isinstance(point, Coord):
        # if point is already a Coord object return it.
        return point
    else:
        return Coord(point[0], point[1])

def to_point(coord):
    '''Converts a Coord object to the points coordinate system'''
    return [coord.row, coord.col]


def get_reachable_rooms(origin, level):
    '''Returns a list of coords specifying the origin of rooms reachable through 1 hallway from room at the provided coordinate. Returns None if the provided coordinate does not match the origin of a room'''
    reachable = []
    for room in level.rooms:
        if origin == room.origin:
            for door in room.doors:
                for hall in level.hallways:
                    if door in hall.doors:
                        reachable += [room.origin for room in hall.rooms if door not in room.doors]
    return reachable

def get_reachable_halls(origin, level):
    '''Returns a list of coords specifying the origin of rooms that are connected through the hallway at the provided coordinate. Returns None if the provided coordinate does not match the origin of a hallway'''
    reachable = []
    for hall in level.hallways:
        if origin == hall.origin:
            reachable += [room.origin for room in hall.rooms]
    return reachable


def check_position(pos, level):
    '''Checks if the provide point is inside the level. If so returns whether it is a hallway or a room, and its respective origin.'''
    row_dimensions = (pos.row, pos.row)
    col_dimensions = (pos.col, pos.col)
    room_dimensions = level.get_level_room_dimensions()
    hall_dimensions = level.get_level_hallway_dimensions()
    pos = None
    # Room or Hallway
    origin_type = None
    room_origin = check_dimensions(row_dimensions, col_dimensions, room_dimensions)
    hall_origin = check_dimensions(row_dimensions, col_dimensions, hall_dimensions)
    if room_origin:
        origin_type = ROOM
        pos = room_origin
    elif hall_origin:
        origin_type = HALLWAY
        pos = hall_origin
    return {'type': origin_type, 'origin': pos}


def coord_radius(pos, dimensions):
    '''Returns a set of coordinates the provided coordinate is at the center'''
    coords = set()
    for ii in range(1, int(round(dimensions.row/2)) + 1):
        for jj in range(1, int(round(dimensions.col/2)) + 1):
            c1 = Coord(pos.row + ii, pos.col + jj)
            c2 = Coord(pos.row + ii, pos.col - jj)
            c3 = Coord(pos.row - ii, pos.col + jj)
            c4 = Coord(pos.row - ii, pos.col - jj)
            c5 = Coord(pos.row, pos.col + jj)
            c6 = Coord(pos.row, pos.col - jj)
            c7 = Coord(pos.row + ii, pos.col)
            c8 = Coord(pos.row - ii, pos.col)
            coords.update([c1, c2, c3, c4, c5, c6, c7, c8])
    return coords


def create_local_player(name):
    '''Helper for instantiating a localPlayer'''
    player_obj = PlayerActor(name)
    return LocalPlayer(name, player_obj=player_obj)
