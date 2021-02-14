#!/usr/bin/env python

import pygame
WHITE = (255,255,255)
BLACK = (0, 0, 0)
GREY = (125, 125, 125)
YELLOW = (255, 225, 125)
WIDTH = 700
HEIGTH = 500
SIZE = 25


# Assuming that dimension given will not be offset from the origin and will just be sized dimensions in x and y.
#   ie. origin = (10, 10) dimensions = (5, 7) The tile boundaries of the room are (10 - 15, 10 - 17)
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

    def check_vertical(self):
        for room in self.rooms:
            for door in room.doors:
                if door.y != self.origin.y or door.y != self.origin.y + self.dimensions.y:
                    return False
        return True

    def check_horizontal(self):
        for room in self.rooms:
            for door in room.doors:
                if door.x != self.origin.x or door.x != self.origin.x + self.dimensions.x:
                    return False
        return True

    # Checks that doors in the hallway are on the same axis. If True they are on the vertical axis. If False horizontal. Otherwise an error message
    def check_vertical_axis(self):
        if self.check_horizontal():
            return False
        elif self.check_vertical():
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

def check_dimensions(x, y, level_dimensions):
    for level in level_dimensions:
        # level is tuple in format ([x_origin, x_origin+dest], [y_origin, y_origin+dest])
        x_origin = level[0][0]
        x_dest = level[0][1]
        y_origin = level[1][0]
        y_dest = level[1][1]
        if x in range(x_origin, x_dest + 1):
            return False
        if y in range(y_origin, y_dest + 1):
            return False
        return True

class Level:
    def __init__(self, rooms, hallways):
        self.rooms = rooms
        self.hallways = hallways

    def check_rooms(self):
        room_dimensions = set()
        hall_dimensions = set()
        for room in self.rooms:
            x = [room.origin.x, room.origin.x + room.dimensions.x]
            y = [room.origin.y, room.origin.y + room.dimensions.y]
            old_room_size = len(room_dimensions)
            room_dimensions.add((x, y))
            # Element not added
            if old_room_size == len(room_dimensions):
                print('Invalid Level: Duplicate rooms')
                return False
        for hall in self.hallways:
            x = [hall.origin.x, hall.origin.x + hall.dimensions.x]
            y = [hall.origin.y, hall.origin.y + hall.dimensions.y]
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
            updated_lvl_dimensions = [level for level in level_dimensions if level == coord]
            if not check_dimensions(coord[0], coord[1], updated_lvl_dimensions):
                print('Invalid Level: Overlapping Room(s) or Hallway(s)')
                return False
        return True

class Tile:
    def __init__(self, x, y, wall=True, item=None):
        self.x = x
        self.y = y
        self.wall = wall 
        self.item = item        


def render_tile(tile):
    return Tile(tile.x*SIZE, tile.y*SIZE, True)

def create_example_room():
    tiles = []
    for i in range(0, int(WIDTH / SIZE)):
        for j in range(0, (int(HEIGTH / SIZE))):
            if j == 0 or j == int(HEIGTH / SIZE) - 1:
                #print(str(i) + ", " + str(j) + "  " + str(HEIGTH / SIZE))
                tiles.append(render_tile(Tile(i, j, True)))
            if (i == 0 or i == int(WIDTH / SIZE) - 1) and (j > 0 and j < int(HEIGTH / SIZE) - 1):
                #print(str(i) + ", " + str(j) + "  " + str(HEIGTH / SIZE))
                tiles.append(render_tile(Tile(i, j, True)))

    return tiles


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGTH), 0, 32)
    pygame.display.set_caption('Snarl')
    screen.fill(WHITE)
    pygame.display.flip()
    tiles = create_example_room();

    room = Room((0, 0), (int(WIDTH / 25), int(HEIGTH / 25)), tiles, (15, 10))
    print(str(tiles))
    # Need to find out how to display graphical programs on wsl
    pygame.draw.rect(screen, GREY, (15 * SIZE, 10 * SIZE, 25, 25))
    while True:
        for tile in room.tiles:
            if tile.wall:
                #print(str((tile.x*SIZE, tile.y*SIZE, SIZE, SIZE)))
                print(str(tile.x) + ", " + str(tile.y))
                pygame.draw.rect(screen, BLACK, (tile.x, tile.y, SIZE, SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (tile.x, tile.y, SIZE, SIZE))
        for item in room.items:
                pygame.draw.circle(screen, YELLOW, render_tile(tile))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()

if __name__ == '__main__':
    main()
