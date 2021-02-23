#!/usr/bin/env python

import sys, os, json
currentdir = os.path.dirname(os.path.realpath(__file__))
tests_dir = os.path.dirname(currentdir)
snarl_dir = os.path.dirname(tests_dir)
game_dir = snarl_dir + '/Game'
from coord import Coord
from room import Room

def main(room_input):
    room_json = json.loads(room_input)
    if room_json['type'] != 'room':
        print('Invalid Args: Type is not room')
        return False
    origin = room_json['origin']
    bounds = room_json['bounds']
    layout = room_json['layout']
    # TODO: Not sure if this order will be consistent
    point = room_json[4]
    origin_coord = Coord(origin[0], origin[1])
    dimensions = Coord(bounds['columns'], bounds['rows'])
    tiles = []
    doors = []
    for xx in range(0, bounds['columns']):
        for yy in range(0, bounds['rows']):
            if layout[xx, yy] == 1:
                tiles.append(Coord(xx, yy))
            if layout[xx, yy] == 2:
                doors.append(Coord(xx, yy))
    room_obj = Room(origin_coord, dimensions, tiles, doors)
    reachable_coords = room_obj.get_reachable_tiles(Coord(point[0], point[1]))
    reachable_tiles = []
    for coord in reachable_coords:
        reachable_tiles.append([coord.x, coord.y])
    if reachable_tiles:
        print('Success: Traversable points from, " {point} ," in room at ", {room_origin}, " are ", {reachable_tiles}', point, origin, reachable_tiles)
    else:
        print('Failure: Point ", {point} , " is not in room at ", {room_origin}', point, origin)
    return reachable_tiles



if __name__ == '__main__':
    room_input = input()
    main(room_input)



