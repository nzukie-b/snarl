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


