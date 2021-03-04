#!/usr/bin/env python
from coord import Coord

def check_hallway(hallway):
    '''Checks that a hallway is valid by checking that the hallway's orientation is either vertical or horizontal.'''
    try:
        hallway.check_orientation()
        return True
    except Exception as err:
        # print(err)
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
        try:
            check_hallway(hall)
        except Exception as err:
            #print("HALLWAY CHECK FAILED")
            return False

    #print("dimension check: " + str(level.check_level_dimensions()))
    return level.check_level_dimensions()

# def check_horizontal(coord1, coord2):
#     '''Checks to determine whether two point are able to be connected by a horizontal path'''
#     i