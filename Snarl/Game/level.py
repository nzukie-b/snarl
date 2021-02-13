#!/usr/bin/env python

import pygame
WHITE = (255,255,255)
BLACK = (0, 0, 0)
YELLOW = (255, 225, 125)
WIDTH = 700
HEIGTH = 500
SIZE = 5


# Assuming that dimension given will not be offset from the origin and will just be sized dimensions in x and y.
#   ie. origin = (10, 10) dimensions = (5, 7) The tile boundaries of the room are (10 - 15, 10, 17)
class Room:
    def __init__(self, origin, dimensions, tiles, doors, items=None):
        self.origin = origin
        self.dimensions = dimensions
        self.tiles = tiles
        self.doors = doors
        self.items = items if items != None else []

    # Validate doors are on a walkable tiles. Does not guarantee that tiles are inside room boundaries.
    def check_doors(self):
        for door in self.doors:
            if door not in self.tiles:
                return False
        return True
    
    # Validate walkable tiles are inside the room boundaries
    def check_tiles(self):
        for tile in self.tiles:
            if tile.x > self.origin.x + self.dimensions.x or tile.y > self.origin.y + self.dimensions.y:
                return False
        return True

    # Validate items are on a walkable tile?
    def check_items(self):
        for item in self.items:
            if item.x not in self.tiles:
                # TODO: Are items on non walkable tiles valid?
                return False
        return True
class Hallway:
    def __init__(self, origin, dimensions, rooms, waypoints=None):
        self.origin = origin
        self.dimensions = dimensions
        self.rooms = rooms
        self.waypoints = waypoints if waypoints != None else []

    def check_rooms_vertical(self):
        for room in self.rooms:
            for door in room.doors:
                if door.y != self.origin.y or door.y != self.origin.y + self.dimensions.y:
                    return False
        return True

    def check_rooms_horizontal(self):
        for room in self.rooms:
            for door in room.doors:
                if door.x != self.origin.x or door.x != self.origin.x + self.dimensions.x:
                    return False
        return True

    # Checks that doors in the hallway are on the same axis. If True they are on the vertical axis. If False horizontal. Otherwise an error message
    def check_vertical_axis(self):
        if self.check_rooms_horizontal():
            return False
        elif self.check_rooms_vertical():
            return True
        else:
            # TODO: Better Error
            print('Invalid Hallway: Doors are not on the same axis')
            raise Exception(self)

def check_hallway(hallway):
    try:
        hallway.check_vertical_axis()
        return True
    except Exception as err:
        print(err)

# Since valid_doors is only checked after valid_tiles is True it is not an issue that check_doors does not guarantee that the walkable tiles are inside the room as check_tiles handles guarantees that 
def check_room(room):
    valid_tiles = room.check_tiles()
    valid_doors = room.check_doors()
    if not valid_tiles:
        print('Invalid Room: Walkable tile(s) outside of room dimensions')
        return False
    if not valid_doors:
        print('Invalid Room: Door(s) outside of walkable tiles')
        return False
    return True
class Tile:
    def __init__(self, x, y, wall=True, item=None):
        self.x = x
        self.y = y
        self.wall = wall 
        self.item = item        


def render_tile(tile):
    return pygame.Rect(tile.x*SIZE, tile.y*SIZE, SIZE, SIZE)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGTH))
    pygame.display.set_caption('Snarl')
    screen.fill(WHITE)
    pygame.display.flip()
    # Need to find out how to display graphical programs on wsl
    while True:
        for tile in tiles:
            if tile.wall:
                pygame.draw.rect(screen, BLACK, render_tile(tile))
            else:
                pygame.draw.rect(screen, WHITE, render_tile(tile))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()

if __name__ == '__main__':
    main()
