#!/usr/bin/env python

import sys, os, json
currentdir = os.path.dirname(os.path.realpath(__file__))
tests_dir = os.path.dirname(currentdir)
snarl_dir = os.path.dirname(tests_dir)
game_dir = snarl_dir + '/Game'
sys.path.append(game_dir)
from coord import Coord
from room import Room

def main(room_input):
    room_json = json.loads(room_input)
    print(room_json[0]['type'])
    if room_json[0]['type'] != 'room':
        print(room_json['type'])
        print('Invalid Args: Type is not room')
        return False
    origin = room_json[0]['origin']
    bounds = room_json[0]['bounds']
    layout = room_json[0]['layout']
    point = room_json[1]
    origin_coord = Coord(origin[0], origin[1])
    dimensions = Coord(bounds['columns'], bounds['rows'])
    tiles = []
    doors = []
    for ii in range(0, bounds['rows']):
        for jj in range(0, bounds['columns']):
            # ii = x jj = y
            if layout[ii][jj] != 0:
                tiles.append(Coord(origin[0] + ii, origin[1] + jj))
            if layout[ii][jj] == 2:
                doors.append(Coord(origin[0] + ii, origin[1] + jj))
    room_obj = Room(origin_coord, dimensions, tiles, doors)

    reachable_coords = room_obj.get_reachable_tiles(Coord(point[0], point[1]))
    reachable_tiles = []
    for coord in reachable_coords:
        reachable_tiles.append([coord.x, coord.y])
    if reachable_tiles:
        print(f'[ Success: Traversable points from, " {point} ," in room at ", {origin}, " are ", {reachable_tiles} ]')
    else:
        print(f'[ Failure: Point ", {point} , " is not in room at ", {origin} ]')
    return reachable_tiles


if __name__ == '__main__':
    room_input = sys.stdin.read().strip()
    main(room_input)



