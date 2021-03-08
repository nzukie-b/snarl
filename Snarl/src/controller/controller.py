#!/usr/bin/env python
import sys, os, json

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from coord import Coord
from utilities import to_coord, to_point
from model.room import Room
from model.hallway import Hallway
from model.level import Level
from model.player import Player
from model.adversary import Adversary
from model.gamestate import GameState


def parse_room_obj(room_input):
    try:
        room_json = json.loads(room_input)
    except TypeError:
        room_json = room_input
    origin = None
    bounds = None
    layout = None
    point = None
    try:
        # [Room, Point] format 
        if room_json[0]['type'] != 'room':
            print('Invalid Args: Type is not room')
            return None
        input_json = room_json[0]
        point = room_json[1]
    except (KeyError, IndexError):
        input_json = room_json
    origin = input_json['origin']
    bounds = input_json['bounds']
    layout = input_json['layout']

    origin_coord = to_coord(origin)
    dimensions = Coord(bounds['rows'], bounds['columns'])
    tiles = []
    doors = []
    for ii in range(0, bounds['rows']):
        for jj in range(0, bounds['columns']):
            # ii = x jj = y
            if layout[ii][jj] != 0:
                tiles.append(Coord(origin[0] + ii, origin[1] + jj))
            if layout[ii][jj] == 2:
                doors.append(Coord(origin[0] + ii, origin[1] + jj))
    return {'coord': to_coord(point) if point else None, 'room': Room(origin_coord, dimensions, tiles, doors)}

def parse_room(room_input):
    parsed_input = parse_room_obj(room_input)
    parsed_coord = parsed_input['coord']
    if not parsed_coord:
        print('Invalid Args: point is missing')
        return None
    room_obj = parsed_input['room']
    if (parsed_coord.row not in range(room_obj.origin.row, room_obj.origin.row + room_obj.dimensions.row + 1)) or (parsed_coord.col not in range(room_obj.origin.col, room_obj.origin.col + room_obj.dimensions.col + 1)):
        print('[ Failure: Point ", {} , " is not in room at ", {} ]'.format([parsed_coord.row, parsed_coord.col], [room_obj.origin.row, room_obj.origin.col]))
        return None
    reachable_coords = room_obj.get_reachable_tiles(parsed_coord)
    reachable_tiles = [to_point(coord) for coord in reachable_coords]
    print('[ Success: Traversable points from, " {} ," in room at, " {} ," are, " {} ]'.format([parsed_coord.row, parsed_coord.col], [room_obj.origin.row, room_obj.origin.col], reachable_tiles))
    return reachable_tiles

def parse_hall(hall_input, rooms):
    try:
        hall_json = json.loads(hall_input)
    except TypeError:
        hall_json = hall_input
    if hall_json['type'] != 'hallway':
        print('Invalid Args: Type is not hallway')
        return None
    from_point = hall_json['from']
    to_point = hall_json['to']
    from_ = to_coord(from_point)
    to = to_coord(to_point)
    waypoints = hall_json['waypoints']
    waypoints_list = [to_coord(waypoint) for waypoint in waypoints]
    rooms_list = [room for room in rooms if from_ in room.doors or to in room.doors]
    return Hallway([from_, to], rooms_list, waypoints_list)
        
def parse_level(level_input):    
    try:
        level_json = json.loads(level_input)
    except TypeError:
        level_json = level_input

    rooms = None
    hallways = None
    objects = None
    point = None
    try:
        if level_json[0]['type'] != 'level':
            print('Invalid Args: Type is not level')
            return None
        input_json = level_json[0]
        point = level_json[1]
    except (KeyError, IndexError):
        input_json = level_json
    rooms = input_json['rooms']
    hallways = input_json['hallways']
    objects = input_json['objects']

    rooms_list = [parse_room_obj(room)['room'] for room in rooms]
    halls_list = [parse_hall(hall, rooms_list) for hall in hallways]

    exit_coord = None
    key_coord = None
    for item in objects:
        posn = item['position']
        if item['type'] == 'key':
            key_coord = to_coord(posn)
        elif item['type'] == 'exit':
            exit_coord = to_coord(posn)

    parsed_level = Level(rooms_list, halls_list, [key_coord], [exit_coord])
    return {'level': parsed_level, 'coord': to_coord(point)}   

def parse_actor(actor_input):
    actor_type = actor_input['type']
    name = actor_input['name']
    coord = to_coord(actor_input['position'])
    if actor_type == 'player':
        return Player(coord, name)
    else:
        return Adversary(coord, name)
def parse_state(state_input):
    try:
        state_json = json.loads(str(state_input))
    except TypeError:
        state_json = state_input
    level = None
    players = []
    adversaries = []
    exit_locked = None

    try:
        if state_json[0]['type'] != 'state':
            print('Invalid Args: Type is not state')
            return None
        input_json = state_json[0]
        name = state_json[1]
        coord = to_coord(state_json[2])
    except (KeyError, IndexError):
        input_json = state_json

    level_input = input_json['level']
    players_input = input_json['players']
    adversaries_input = input_json['adversaries']
    exit_locked = input_json['exit_locked']

    level = parse_level(level_input)['level']
    players = [parse_actor(actor_input) for actor_input in players_input]
    adversaries = [parse_actor(actor_input) for actor_input in adversaries_input]
    state = GameState(level, players, adversaries, exit_locked)
    return {'state': state, 'name': name if name else None, 'coord': coord if coord else None}
    