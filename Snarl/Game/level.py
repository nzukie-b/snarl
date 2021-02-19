#!/usr/bin/env python

import pygame
from coord import Coord
from room import Room
from hallway import Hallway
from utilities import check_dimensions
from constants import SIZE, HEIGTH, WIDTH, WHITE, BLACK, YELLOW
SCREEN = pygame.display.set_mode((WIDTH, HEIGTH), 0, 32)
SCREEN.fill(WHITE)
pygame.display.set_caption('Snarl')

class Tile:
    def __init__(self, x, y, wall=True, item=None):
        self.x = x * SIZE
        self.y = y * SIZE
        self.wall = wall 
        self.item = item        


class Level:
    def __init__(self, rooms, hallways):
        self.rooms = rooms
        self.hallways = hallways

    #  Checks that there are not rooms/hallways sharing coordinates, or having overlapping dimensions
    def check_level_dimensions(self):
        '''Checks that this level has no rooms/hallways sharing coodinates or having overlapping dimension'''
        room_dimensions = set()
        hall_dimensions = set()
        for room in self.rooms:
            x = (room.origin.x, room.origin.x + room.dimensions.x)
            y = (room.origin.y, room.origin.y + room.dimensions.y)
            old_room_size = len(room_dimensions)
            room_dimensions.add((x, y))
            # Element not added
            if old_room_size == len(room_dimensions):
                print('Invalid Level: Duplicate rooms')
                return False
        for hall in self.hallways:
            x = (hall.origin.x, hall.origin.x + hall.dimensions.x)
            y = (hall.origin.y, hall.origin.y + hall.dimensions.y)
            old_hall_size = len(hall_dimensions)
            hall_dimensions.add((x, y)) 
            if old_hall_size == len(hall_dimensions):
                print('Invalid Level: Duplicate hallways')
                return False
        level_size = len(room_dimensions) + len(hall_dimensions)
        level_dimensions = room_dimensions.union(hall_dimensions)
        if level_size != len(level_dimensions):
            print('Invalid Level: Hallway or Room sharing coordinates')
            return False
        for coord in level_dimensions:
            # Remove the coordinate used for comparison from the set to avoid counting itself.
            updated_lvl_dimensions = [level for level in level_dimensions if level != coord]
            if not check_dimensions(coord[0], coord[1], updated_lvl_dimensions):
                print('Invalid Level: Overlapping Room(s) or Hallway(s)')
                return False
        return True


def render_tile(tile):
    '''Returns a rectangle for the provided Tile to be rendered on the view'''
    return pygame.Rect(tile.x, tile.y, SIZE, SIZE)

def render_room(room):
    '''Renders tiles for the provided Room, and returns the list of the created tiles.'''
    tiles = []
    for ii in range(room.origin.x, room.origin.x + room.dimensions.x + 1):
        for jj in range(room.origin.y, room.origin.y + room.dimensions.y + 1):
            coord = Coord(ii, jj)
            tile = Tile(ii, jj)
            tiles.append(tile)
            if coord in room.doors:
                pygame.draw.rect(SCREEN, GREY, render_tile(tile))
            elif coord in room.items:
                pygame.draw.circle(SCREEN, YELLOW, (tile.x + SIZE / 2, tile.y + SIZE / 2), SIZE / 2)
            elif coord in room.tiles:
                pygame.draw.rect(SCREEN, WHITE, render_tile(tile))
            else:
                pygame.draw.rect(SCREEN, BLACK, render_tile(tile))
    return tiles

def render_hallway(hallway, orientation):
    '''Renders tiles for the provided hallway based on the hallway's orientaion, and returns the list of the created tiles.'''
    try :
        x_boundary = hallway.origin.x + hallway.dimensions.x
        y_boundary = hallway.origin.y + hallway.dimensions.y
        tiles = []
        for ii in range(hallway.origin.x, x_boundary + 1):
            for jj in range(hallway.origin.y, y_boundary + 1):
                tile = Tile(ii, jj)
                tiles.append(tile)
                pygame.draw.rect(SCREEN, WHITE, render_tile(tile))
                # Walls aren't defined from the dimensions we assume the provided dimensions are all walkable
                if orientation == False:
                    # Vertical path hallway case
                    left_wall = Tile(hallway.origin.x - 1, jj)
                    right_wall = Tile(x_boundary + 1, jj)
                    pygame.draw.rect(SCREEN, BLACK, render_tile(left_wall))
                    pygame.draw.rect(SCREEN, BLACK, render_tile(right_wall))
                elif orientation == True:
                    # Horizontal path hallway
                    upper_wall = Tile(ii, hallway.origin.y - 1)
                    lower_wall = Tile(ii, y_boundary + 1)
                    pygame.draw.rect(SCREEN, BLACK, render_tile(upper_wall))
                    pygame.draw.rect(SCREEN, BLACK, render_tile(lower_wall))
        return tiles
    except Exception as err :
        print('Error: Attempting to render invalid hallway. Object: ', err)

def render_level(level):
    for hall in level.hallways:
        render_hallway(hall, hall.check_orientation())
    for room in level.rooms:
        render_room(room)

def main():
    pygame.init()
    pygame.display.flip()
    #Room 1 example
    tiles = [Coord(7, 6),Coord(7, 8),Coord(7, 9),Coord(7, 10), Coord(6, 6), Coord(6, 8), Coord(8, 9), Coord(8,6), Coord(8, 7), Coord(8,8), Coord(8, 9), Coord(8, 10), Coord(9, 6), Coord(9, 7), Coord(9,8) ]
    start = Coord(5, 5)
    dimensions = Coord(5, 5)
    doors = [Coord(8,10), Coord(7, 10), Coord(6, 10)]
    items = [Coord(6, 6), Coord(7, 8)]
    room = Room(start, dimensions, tiles, doors, items)
    hall_start = Coord(6, 11)
    hall = Hallway(hall_start, Coord(2, 3), [room])
    #Room 2 example
    tiles1 = [Coord(7, 14), Coord(7, 17), Coord(7, 18), Coord(6, 17), Coord(8, 18), Coord(8, 15), 
                Coord(6, 15), Coord(7, 15), Coord(7, 15), Coord(9, 17), Coord(9, 16), Coord(9, 15), Coord (9, 14), Coord(6, 16)]
    start1 = Coord(5, 14)
    dimensions1 = Coord(5, 5)
    doors1 = [Coord(8, 14), Coord(7, 14), Coord(6, 14), Coord(9,14)]
    items1 = [Coord(8, 14), Coord(7, 17)]
    room1 = Room(start1, dimensions1, tiles1, doors1, items1)

    while True:
        render_level(Level([room, room1], [hall]))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

if __name__ == '__main__':
    main()
