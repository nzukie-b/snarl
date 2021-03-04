#!/usr/bin/env python
import copy
from coord import Coord
from utilities import check_dimensions
from model.room import Room
from model.hallway import Hallway
from model.player import Player
from model.adversary import Adversary

class Level:
    def __init__(self, rooms, hallways, keys=[], exits=[]):
        self.rooms = rooms
        self.hallways = hallways
        self.keys = keys
        self.exits = exits
    
    def __str__(self):
        rooms_str = [str(room) for room in self.rooms]
        halls_str = [str(hall) for hall in self.hallways]
        return '{{"rooms": {}, "hallways": {}}}'.format(rooms_str, halls_str)

    def get_level_room_dimensions(self):
        '''Returns a set of ((x_origin, x_dest), (y_origin, y_dest)) representing the dimension boundaries of each room in the level'''
        room_dimensions = set()
        for room in self.rooms:
            row = (room.origin.row, room.origin.row + room.dimensions.row)
            col = (room.origin.col, room.origin.col + room.dimensions.col)
            old_room_size = len(room_dimensions)
            room_dimensions.add((row, col))
            # Element not added
            if old_room_size == len(room_dimensions):
                print('Invalid Level: Duplicate rooms')
                return None
        return room_dimensions

    def get_level_hallway_dimensions(self):
        '''Returns a set of ((x_origin, x_dest), (y_origin, y_dest)) representing the dimension boundaries of each hallway in the level'''
        hall_dimensions = set()
        for hall in self.hallways:
            row = (hall.origin.row, hall.origin.row + hall.dimensions.row)
            col = (hall.origin.col, hall.origin.col + hall.dimensions.col)
            old_hall_size = len(hall_dimensions)
            hall_dimensions.add((row, col)) 
            if old_hall_size == len(hall_dimensions):
                print('Invalid Level: Duplicate hallways')
                return None
        return hall_dimensions   

    #  Checks that there are not rooms/hallways sharing coordinates, or having overlapping dimensions
    def check_level_dimensions(self):
        '''Checks that this level has no rooms/hallways sharing coodinates or having overlapping dimensions'''
        room_dimensions = self.get_level_room_dimensions()
        hall_dimensions = self.get_level_hallway_dimensions()
        if not hall_dimensions or not room_dimensions:
            return False
        level_size = len(room_dimensions) + len(hall_dimensions)
        level_dimensions = room_dimensions.union(hall_dimensions)
        if level_size != len(level_dimensions):
            print('Invalid Level: Hallway or Room sharing coordinates')
            return False
        for coord in level_dimensions:
            # Remove the coordinate used for comparison from the set to avoid counting itself.
            updated_lvl_dimensions = [level for level in level_dimensions if level != coord]
            if check_dimensions(coord[0], coord[1], updated_lvl_dimensions):
                print('Invalid Level: Overlapping Room(s) or Hallway(s)')
                return False
        return True

    def info_at_coord(self, coord):
        '''Checks if the tile at the provided coordinate is within the bounds of the level. If so, it will return and object/dictionary with the following info
            - whether the tile is traversable : ['traversable']
            - whether the tile it references contains a key or an exit : ['object']
            - if it is a hallway, or room : ['type']
            - if a hallway the origins of the connecting rooms | if a room the origins of neighboring rooms, that is, the rooms that are one hallway removed from the current room : ['reachable']'''
        result = {
            'traversable': None,
            'object': 'null',
            'type': 'void', 
            'reachable': []
        }
        row_dimensions = (coord.row, coord.row)
        col_dimensions = (coord.col, coord.col)
        room_dimensions = self.get_level_room_dimensions()
        hall_dimensions = self.get_level_hallway_dimensions()
        if not check_dimensions(row_dimensions, col_dimensions, room_dimensions.union(hall_dimensions)):
            # Provided coordinate is not within the bounds of the level
            result['traversable'] = False
            result['object'] == 'null'
        else:
            # Point is guaranteed to be within level dimensions
            origin = None
            #False if Hallway, True if Room, None otherwise
            is_room = None
            room_origin = check_dimensions(row_dimensions, col_dimensions, room_dimensions)
            hall_origin = check_dimensions(row_dimensions, col_dimensions, hall_dimensions)
            if room_origin:
                is_room = True
                origin = room_origin
            elif hall_origin:
                is_room = False
                origin = hall_origin
            if is_room == True:
                for room in self.rooms:
                    if origin == room.origin:
                        print(room.origin, room.dimensions)
                        # print(room.doors[0].x, room.doors[0].y)
                        result['type'] = 'room'
                        #TODO: Change both traversables to use methods. create is_reachable method to return a boolean
                        result['traversable'] = coord in room.tiles
                        reachable = []
                        for door in room.doors:
                            # print(len(room.doors))
                            for hall in self.hallways:
                                if door in hall.doors:
                                    print('hall_room_origins')
                                    for hall_room in hall.rooms:
                                        print(hall_room.origin)
                                    reachable += [[room.origin.row, room.origin.col] for room in hall.rooms if door not in room.doors]
                        # # Go through the doors in room1 and find the connecting hall. Add the origin of all connecting rooms from the found hall to reachable
                        #     for hall_room in hall.rooms:
                        #         for door in room.doors:
                        #             if door in hall_room.doors:
                        #                 # print(door)
                        #                 # print(hall_room.origin, hall_room.dimensions)
                                        
                        #                 # for connected_room in [hall for hall in hall.rooms if hall.room.origin != origin]:
                        #                 for connected_room in hall.rooms:

                        #                     if [connected_room.origin.x, connected_room.origin.y] not in reachable: reachable.append([connected_room.origin.x, connected_room.origin.y])
                        #                 for connected_waypoint in hall.waypoints:
                        #                     if [connected_waypoint.origin.x, connected_waypoint.origin.y] not in reachable: reachable.append([connected_waypoint.origin.x, connected_waypoint.origin.y])
                        result['reachable'] = reachable
            elif is_room == False:
                for hall in self.hallways:
                    if origin == hall.origin:
                        result['type'] = 'hallway'
                        traversable = coord.row in range(hall.origin.row, hall.origin.row + hall.dimensions.row + 1) and coord.col in range(hall.origin.col, hall.origin.col + hall.dimensions.col + 1)
                        result['traversable'] = traversable
                        reachable = [[room.origin.row, room.origin.col] for room in hall.rooms]
                        # for room in hall.rooms:
                        #     reachable.append([room.origin.row, room.origin.col])
                        result['reachable'] = reachable
            if coord in self.exits:
                result['object'] = 'exit'
            if coord in self.keys:
                result['object'] = 'key'
        return result


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
        print(str(tile.row) + " " + str(tile.col) + " in doors " + str(tile in first.doors))
        print(str(tile.row) + " " + str(tile.col) + " in items " + str(tile in first.items))
        if tile not in first.doors and tile not in first.items:
            print("ADD TO LIST: " + str(tile.row) + " " + str(tile.col))
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
        print("ADDP: " + str(cur_tile.row) + " " + str(cur_tile.col))
        players.append(Player(Coord(cur_tile.row, cur_tile.col), "Bruh " + str(i), 3))

    for i in range(num_adversaries):
        cur_adversary_tile = last_room.tiles[i]
        print("ADDA: " + str(cur_adversary_tile.row) + " " + str(cur_adversary_tile.col))
        adversaries.append(Adversary(Coord(cur_adversary_tile.row, cur_adversary_tile.col), "Evil Bruh " + str(i), 3))

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


