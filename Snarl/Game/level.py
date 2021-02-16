#!/usr/bin/env python

import pygame
WHITE = (255,255,255)
BLACK = (0, 0, 0)
GREY = (125, 125, 125)
YELLOW = (255, 225, 125)
WIDTH = 700
HEIGTH = 500
SIZE = 25
SCREEN = pygame.display.set_mode((WIDTH, HEIGTH), 0, 32)
SCREEN.fill(WHITE)
pygame.display.set_caption('Snarl')


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Coord):
            return self.x == other.x and self.y == other.y
        return False


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


# Check the orientation of the Hall. If True it is horizontal if False it is vertical otherwise an error is thrown
    def check_orientation(self):
        is_horizontal = None
        for room in self.rooms:
            for door in room.doors:
                if (door.y == self.origin.y or door.y == self.origin.y + self.dimensions.y) and (self.origin.x < door.x < self.origin.x + self.dimensions.x):
                    if is_horizontal is False:
                        raise Exception(self)
                    is_horizontal = True
                elif (door.x == self.origin.x or door.x == self.origin.x + self.dimensions.x ) and (self.origin.y < door.y < self.origin.y + self.dimensions.y):
                    if is_horizontal is True:
                        raise Exception(self)
                    is_horizontal = False                        
        return is_horizontal


# Checks that a hallway is either vertical or horizontal 
def check_hallway(hallway):
    try:
        hallway.check_orientation()
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


# Checks that the provided coordinates are not within the provided coordinates. True if the provided coordinates do not both fall the level dimensions
def check_dimensions(x, y, level_dimensions):
    for level in level_dimensions:
        # level is tuple in format ([x_origin, x_origin+dest], [y_origin, y_origin+dest]), Created in check_room
        x_origin = level[0][0]
        x_dest = level[0][1]
        y_origin = level[1][0]
        y_dest = level[1][1]
        if x in range(x_origin, x_dest + 1) and y in range(y_origin, y_dest + 1):
            return False
        return True


class Level:
    def __init__(self, rooms, hallways):
        self.rooms = rooms
        self.hallways = hallways

#  Checks that there are not rooms/hallways sharing coordinates, or having overlapping dimensions
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
            updated_lvl_dimensions = [level for level in level_dimensions if level != coord]
            if not check_dimensions(coord[0], coord[1], updated_lvl_dimensions):
                print('Invalid Level: Overlapping Room(s) or Hallway(s)')
                return False
        return True


class Tile:
    def __init__(self, x, y, wall=True, item=None):
        self.x = x * SIZE
        self.y = y * SIZE
        self.wall = wall 
        self.item = item        

def create_example_tiles():
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


def create_example_items():
    items = []
    for i in range(0, int(WIDTH / SIZE)):
        for j in range(0, (int(HEIGTH / SIZE))):
            if ((i == 5 and j == 10) or
                (i == 17 and j == 17) or
                    (i == 6 and j == 3)):
                items.append(Coord(i, j))
    return items


def render_tile(tile):
    return pygame.Rect(tile.x, tile.y, SIZE, SIZE)

# Renders tiles for a room, annd returns a list of the created tiles.
def render_room(room):
    tiles = []
    for ii in range(room.origin.x, room.origin.x + room.dimensions.x + 1):
        for jj in range(room.origin.y, room.origin.y + room.dimensions.y + 1):
            coord = Coord(ii, jj)
            tile = Tile(ii, jj)
            tiles.append(tile)
            if coord in room.doors:
                pygame.draw.circle(SCREEN, YELLOW, (tile.x + SIZE/2, tile.y + SIZE/2), SIZE/2)
            elif coord in room.tiles:
                pygame.draw.rect(SCREEN, WHITE, render_tile(tile))
            else:
                pygame.draw.rect(SCREEN, BLACK, render_tile(tile))
    return tiles

# Renders tiles for a hallway, and returns a list of the created tiles.
def render_hallway(hallway, orientation):
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
                if orientation == True:
                    # Horizontal path hallway case
                    left_wall = Tile(hallway.origin.x - 1, jj)
                    right_wall = Tile(x_boundary + 1, jj)
                    pygame.draw.rect(SCREEN, BLACK, render_tile(left_wall))
                    pygame.draw.rect(SCREEN, BLACK, render_tile(right_wall))
                elif orientation == False:
                    # Vertical path hallway
                    upper_wall = Tile(ii, hallway.origin.y - 1)
                    lower_wall = Tile(ii, y_boundary + 1)
                    pygame.draw.rect(SCREEN, BLACK, render_tile(upper_wall))
                    pygame.draw.rect(SCREEN, BLACK, render_tile(lower_wall))
        return tiles
    except Exception as err :
        print('Error: Attempting to render invalid hallway. Object: ', err)

def main():
    pygame.init()
    pygame.display.flip()
    tiles = [Coord(7, 6),Coord(7, 8),Coord(7, 9),Coord(7, 10), Coord(6, 6), Coord(6, 8), Coord(8, 9), Coord(8,6), Coord(8, 7), Coord(8,8), Coord(8, 9), Coord(8, 10)]
    start = Coord(5, 5)
    dimensions = Coord(5, 5)
    doors = [Coord(8,10), Coord(7, 10), Coord(6, 10)]
    room = Room(start, dimensions, tiles, doors)
    hall_start = Coord(6, 10)
    hall = Hallway(hall_start, Coord(2, 3), [room])
    print(hall.check_orientation())
    


    # pygame.draw.rect(screen, GREY, (15 * SIZE, 10 * SIZE, 25, 25))
    while True:
        render_hallway(hall, hall.check_orientation())

        render_room(room)
        # for ii in range(room.origin.x, room.origin.x + room.dimensions.x):
        #     for jj in range(room.origin.y, room.origin.y + room.dimensions.y):
        #         coord = Coord(ii, jj)
        #         tile = Tile(ii, jj)
        #         if coord in room.tiles:
        #             pygame.draw.rect(SCREEN, WHITE, render_tile(tile))
        #         else:
        #             pygame.draw.rect(SCREEN, BLACK, (coord.x*SIZE, coord.y*SIZE, SIZE, SIZE))
        pygame.display.update()
        # for tile in room.tiles:
        #     if tile.wall:
        #         #print(str((tile.x*SIZE, tile.y*SIZE, SIZE, SIZE)))
        #         #print(str(tile.x) + ", " + str(tile.y))
        #         pygame.draw.rect(screen, BLACK, (tile.x, tile.y, SIZE, SIZE))
        #     else:
        #         pygame.draw.rect(screen, WHITE, (tile.x, tile.y, SIZE, SIZE))
        # for item in room.items:
        #     pygame.draw.circle(screen, YELLOW, (item.x, item.y), SIZE/2, SIZE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

if __name__ == '__main__':
    main()
