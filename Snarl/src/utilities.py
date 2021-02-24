#!/usr/bin/env python
import pygame
from coord import Coord
from room import Room
from hallway import Hallway
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
    '''Checks that the provided coordinates, are not withing the level dimensions. True if the coordinates are not both within level dimensions'''
    x_start = x_dimensions[0]
    x_end = x_dimensions[1]
    y_start = y_dimensions[0]
    y_end = y_dimensions[1]
    for level in level_dimensions:
        # level is tuple in format ((x_origin, x_origin+dest), (y_origin, y_origin+dest)), Created in check_room
        level_x_origin = level[0][0]
        level_x_dest = level[0][1]
        level_y_origin = level[1][0]
        level_y_dest = level[1][1]
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end +1):
                if x in range(level_x_origin, level_x_dest + 1) and y in range(level_y_origin, level_y_dest + 1):
                    return False
        return True

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



# def create_example_tiles():
#     tiles = []
#     for i in range(0, int(WIDTH / SIZE)):
#         for j in range(0, (int(HEIGTH / SIZE))):
#             if j == 0 or j == int(HEIGTH / SIZE) - 1:
#                 #print(str(i) + ", " + str(j) + "  " + str(HEIGTH / SIZE))
#                 tiles.append(render_tile(Tile(i, j, True)))
#             if (i == 0 or i == int(WIDTH / SIZE) - 1) and (j > 0 and j < int(HEIGTH / SIZE) - 1):
#                 #print(str(i) + ", " + str(j) + "  " + str(HEIGTH / SIZE))
#                 tiles.append(render_tile(Tile(i, j, True)))
#     return tiles


def create_example_items():
    items = []
    for i in range(0, int(WIDTH / SIZE)):
        for j in range(0, (int(HEIGTH / SIZE))):
            if ((i == 5 and j == 10) or
                (i == 17 and j == 17) or
                    (i == 6 and j == 3)):
                items.append(Coord(i, j))
    return items

