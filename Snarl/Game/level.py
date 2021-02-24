#!/usr/bin/env python

import pygame
from coord import Coord
from room import Room
from hallway import Hallway
from utilities import check_dimensions
from constants import SIZE, HEIGTH, WIDTH, WHITE, BLACK, YELLOW, GREY, BLUE, RED
from player import Player
from adversary import Adversary
import copy
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


class GameState:
    def __init__(self, players, adversaries, level_exited=False):
        self.players = players
        self.adversaries = adversaries
        self.level_exited = level_exited


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


def render_players(players):
    for player in players:
        pygame.draw.circle(SCREEN, BLUE, (player.pos.x + SIZE / 2, player.pos.y + SIZE / 2), SIZE / 2)


def render_adversaries(adversaries):
    #print(str(adversaries))
    for adversary in adversaries:
        pygame.draw.circle(SCREEN, RED, (adversary.pos.x + SIZE / 2, adversary.pos.y + SIZE / 2), SIZE / 2)


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


def remove_doors_and_items_from_rooms(first):
    first_rm = copy.deepcopy(first)
    first_rm_removed = []

    print("1 " + str(len(first.tiles)))
    print("2 " + str(len(first_rm.tiles)))

    for tile in first_rm.tiles:
        print(str(tile.x) + " " + str(tile.y) + " in doors " + str(tile in first.doors))
        print(str(tile.x) + " " + str(tile.y) + " in items " + str(tile in first.items))
        if tile not in first.doors and tile not in first.items:
            print("ADD TO LIST: " + str(tile.x) + " " + str(tile.y))
            first_rm_removed.append(tile)

    print("3 " + str(len(first.tiles)))
    print("4 " + str(len(first_rm.tiles)))

    return Room(first_rm.origin, first_rm.dimensions, first_rm_removed, first_rm.doors, first_rm.items)



def create_initial_game_state(level, num_players, num_adversaries):
    players = []
    adversaries = []

    last_room = remove_doors_and_items_from_rooms(level.rooms[len(level.rooms) - 1])
    first_room = remove_doors_and_items_from_rooms(level.rooms[0])

    for i in range(num_players):
        cur_tile = first_room.tiles[i]
        print("ADDP: " + str(cur_tile.x) + " " + str(cur_tile.y))
        players.append(Player(Coord(cur_tile.x, cur_tile.y), "Bruh " + str(i), 3))

    for i in range(num_adversaries):
        cur_adversary_tile = last_room.tiles[i]
        print("ADDA: " + str(cur_adversary_tile.x) + " " + str(cur_adversary_tile.y))
        adversaries.append(Adversary(Coord(cur_adversary_tile.x, cur_adversary_tile.y), "Evil Bruh " + str(i), 3))

    #print(str(adversaries))

    return [players, adversaries]


def update_game_state(new_players_locs, new_adversary_locs, new_players_healths, new_adversary_healths, level_exit_status):
    """
    Replaces the current gamestate with a new gamestate made up of the updated values for all of the game attributes.
    :param new_players_locs: [Coord]
    :param new_adversary_locs: [Coord]
    :param new_players_healths: [int]
    :param new_adversary_healths: [int]
    :param level_exit_status: boolean
    :return:
    """
    players = []
    adversaries = []

    for i in range(len(new_players_locs)):
        players.append(Player(new_adversary_locs[i], "Bruh " + str(i), new_players_healths[i]))

    for i in range(len(new_adversary_locs)):
        adversaries.append(Adversary(new_adversary_locs[i], "Evil Bruh " + str(i), new_adversary_healths[i]))

    return GameState(players, adversaries)


def main():
    pygame.init()
    pygame.display.flip()

    #Room 1 example
    tiles = [Coord(7, 6),Coord(7, 8),Coord(7, 9),Coord(7, 10), Coord(6, 6), Coord(6, 8), Coord(8, 9),
                 Coord(8,6), Coord(8, 7), Coord(8,8), Coord(8, 9), Coord(8, 10), Coord(9, 6), Coord(9, 7), Coord(9,8) ]
    start = Coord(5, 5)
    dimensions = Coord(5, 5)
    doors = [Coord(8,10), Coord(7, 10), Coord(6, 10)]
    items = [Coord(6, 6), Coord(7, 8)]
    room = Room(start, dimensions, tiles, doors, items)
    hall_start = Coord(6, 11)
    hall = Hallway(hall_start, Coord(2, 3), [room])
    #Room 2 example
    tiles1 = [Coord(7, 14), Coord(7, 17), Coord(7, 18), Coord(6, 17), Coord(8, 18), Coord(8, 15), 
                Coord(6, 15), Coord(7, 15), Coord(7, 15), Coord(9, 17), Coord(9, 16), Coord(9, 15), Coord(6, 16)]
    start1 = Coord(5, 14)
    dimensions1 = Coord(5, 5)
    doors1 = [Coord(8, 14), Coord(7, 14), Coord(6, 14)]
    items1 = [Coord(8, 15), Coord(7, 17)]
    room1 = Room(start1, dimensions1, tiles1, doors1, items1)

    gs_info = create_initial_game_state(Level([room, room1], [hall]), 3, 3)
    gamestate = GameState(gs_info[0], gs_info[1])



    while True:
        render_level(Level([room, room1], [hall]))
        render_players(gamestate.players)
        render_adversaries(gamestate.adversaries)
        pygame.display.update()
        #gamestate = update_game_state([], [], [], [], False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

if __name__ == '__main__':
    main()
