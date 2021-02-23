#!/usr/bin/env python

import sys, os, json
currentdir = os.path.dirname(os.path.realpath(__file__))
tests_dir = os.path.dirname(currentdir)
snarl_dir = os.path.dirname(tests_dir)
game_dir = snarl_dir + '/Game'
from coord import Coord
from room import Room

class Bounds:
    def __init__(self, rows, cols):
        self.rows = rows
        self.columns = cols

class Room:
    def __init__(self, origin, bounds, layout):
        self.type =  'room'
        self.origin = origin
        self.bounds = bounds
        self.layout = layout



def main():
    room_json = input()
    room_obj = json.loads(room_json)
    if room_obj['type'] != 'room':
        print('Invalid Args: Type is not room')
        return False
    origin = room_obj['origin']
    bounds = room_obj['bounds']
    layout = room_obj['layout']
    # TODO: Not sure if this order will be consistent
    point = room_obj[4]
    origin_coord = Coord(origin[0], origin[1])
    dimensions = Coord(bounds['columns'], bounds['rows'])
    # for i in range(0, bounds['col'])

