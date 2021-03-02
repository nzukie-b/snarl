#!/usr/bin/env python
import sys, os, json
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from coord import Coord
from model.room import Room
from model.hallway import Hallway
from level import Level

def parse_room_obj(room_input):
    room_json = json.loads(room_input)
    origin = None
    bounds = None
    layout = None
    point = None
    try:
        # [Room, Point] format 
        if room_json[0]['type'] != 'room':
            print(room_json['type'])
            print('Invalid Args: Type is not room')
            return None
        origin = room_json[0]['origin']
        bounds = room_json[0]['bounds']
        layout = room_json[0]['layout']
        point = room_json[1]
    except IndexError:
        origin = room_json['origin']
        bounds = room_json['bounds']
        layout = room_json['layout']

    origin_coord = Coord(origin[0], origin[1])
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
    return {'point': point, 'room': Room(origin_coord, dimensions, tiles, doors)}


def parse_room(room_input):
    parsed_input = parse_room_obj(room_input)
    point = parsed_input['point']
    if not point:
        print('Invalid Args: point is missing')
        return None
    room_obj = parsed_input['room']
    if (point[0] not in range(room_obj.origin.x, room_obj.origin.x + room_obj.dimensions.x + 1)) or (point[1] not in range(room_obj.origin.y, room_obj.origin.y + room_obj.dimensions.y + 1)):
        print('[ Failure: Point ", {} , " is not in room at ", {} ]'.format(point, [room_obj.origin.x, room_obj.origin.y]))
        return None
    reachable_coords = room_obj.get_reachable_tiles(Coord(point[0], point[1]))
    reachable_tiles = []
    for coord in reachable_coords:
        reachable_tiles.append([coord.x, coord.y])
    print('[ Success: Traversable points from, " {} ," in room at, " {} ," are, " {} ]'.format(point, [room_obj.origin.x, room_obj.origin.y], reachable_tiles))
    return reachable_tiles
    

def parse_hall(hall_input, rooms):
    hall_json = json.loads(hall_input)
    if hall_json['type'] != 'hallway':
        print('Invalid Args: Type is not hallway')
        return None
    from_ = hall_json['from']
    to = hall_json['to']
    from_coord = Coord(from_[0], from_[1])
    to_coord = Coord(to[0], to[1])
    waypoints = hall_json['waypoints']
    waypoints_coords = [Coord(waypoint[0], waypoint[1]) for waypoint in waypoints]
    
    is_horizontal = from_coord.y == to_coord.y and from_coord.x != to_coord.x
    hall_boundaries = None
    origin = None
    dimensions = None
    if is_horizontal:
        # From and To are tiles within a room so hall boundaries do not include them
        hall_boundaries = (min(from_coord.x, to_coord.x) + 1, max(from_coord.x, to_coord.x) - 1)
        origin = Coord(hall_boundaries[0], from_coord.y)
        # For now halls are stated to only be a single tile wide, but width could be co
        dimensions = Coord(hall_boundaries[1] - hall_boundaries[0], 1)
    else:
        hall_boundaries = (min(from_coord.y, to_coord.y) + 1, max(from_coord.y, to_coord.y) - 1)
        origin = Coord(from_coord.x, hall_boundaries[0])
        dimensions = Coord(1, hall_boundaries[1] - hall_boundaries[0])
    
    rooms_list = []
    waypoints_list = []
    for room in rooms:
        for door in room.doors:
            if door == to_coord or door == from_coord:
                rooms_list.append(room)
            # Doors are considered to be inside a room each waypoint coord should correspond to a door in a room.
            for waypoint in waypoints_coords:
                if door == waypoint:
                    waypoints_list.append(room)
                    
    return Hallway(origin, dimensions, rooms, waypoints_list)
        
def parse_level(level_input):
    level_json = json.loads(level_input)
    if level_json['type'] != 'level':
        print('Invalid Args: Type is not level')
        return None
    rooms = level_json['rooms']
    hallways = level_json['hallways']
    objects = level_json['objects']

    rooms_list = []
    for room in rooms:
        parsed_room = parse_room_obj(room)
        rooms_list.append(parsed_room['room'])

    halls_list = []
    for hall in hallways:
        parsed_hall = parse_hall(hall)
        halls_list.append(parsed_hall)

    key_coord = None
    exit_coord = None
    for item in objects:
        posn = item['position']
        if item['type'] == 'key':
            key_coord = Coord(posn[0], posn[1])
        elif item['type'] == 'door':
            exit_coord = Coord(posn[0], posn[1])

    parsed_level = Level(rooms_list, halls_list, [key_coord], [exit_coord])
    return parsed_level