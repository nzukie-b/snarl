#!/usr/bin/env python
import sys, os, json

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from game.gameManager import GameManager
from coord import Coord
# from constants import ADVERSARIES, BOUNDS, COLS, COORD, EXIT_LOCKED, FROM, HALLWAY, HALLWAYS, LAYOUT, MANAGER, MAX_TURNS, OBJECTS, ORIGIN, PLAYERS, POS, ROOM, LEVEL, ROOMS, ROWS, STATE, KEY, EXIT, MOVES, NAME, TO, TYPE, WAYPOINTS
from constants import *
from utilities import to_coord, to_point, check_position, coord_radius, streaming_iterload
from model.room import Room
from model.item import Item
from model.hallway import Hallway
from model.level import Level
from model.player import PlayerActor
from model.adversary import AdversaryActor
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
        if room_json[0][TYPE] != ROOM:
            print('Invalid Args: Type is not room')
            return None
        input_json = room_json[0]
        point = room_json[1]
    except (KeyError, IndexError):
        input_json = room_json
    origin = input_json[ORIGIN]
    bounds = input_json[BOUNDS]
    layout = input_json[LAYOUT]

    origin_coord = to_coord(origin)
    dimensions = Coord(bounds[ROWS], bounds[COLS])
    tiles = []
    doors = []
    for ii in range(0, bounds[ROWS]):
        for jj in range(0, bounds[COLS]):
            # ii = x jj = y
            if layout[ii][jj] != 0:
                tiles.append(Coord(origin[0] + ii, origin[1] + jj))
            if layout[ii][jj] == 2:
                doors.append(Coord(origin[0] + ii, origin[1] + jj))
    return {COORD: to_coord(point) if point else None, ROOM: Room(origin_coord, dimensions, tiles, doors)}

def parse_room(room_input):
    parsed_input = parse_room_obj(room_input)
    parsed_coord = parsed_input[COORD]
    if not parsed_coord:
        print('Invalid Args: point is missing')
        return None
    room_obj = parsed_input['room']
    if (parsed_coord.row not in range(room_obj.origin.row, room_obj.origin.row + room_obj.dimensions.row + 1)) or (parsed_coord.col not in range(room_obj.origin.col, room_obj.origin.col + room_obj.dimensions.col + 1)):
        print('[ Failure: Point ", {} , " is not in room at ", {} ]'.format(to_point(parsed_coord), to_point(room_obj.origin)))
        return None
    reachable_coords = room_obj.get_reachable_tiles(parsed_coord)
    reachable_tiles = [to_point(coord) for coord in reachable_coords]
    print('[ Success: Traversable points from, " {} ," in room at, " {} ," are, " {} ]'.format(to_point(parsed_coord), to_point(room_obj.origin), reachable_tiles))
    return reachable_tiles

def parse_hall(hall_input, rooms):
    try:
        hall_json = json.loads(hall_input)
    except TypeError:
        hall_json = hall_input
    if hall_json[TYPE] != HALLWAY:
        print('Invalid Args: Type is not hallway')
        return None
    from_point = hall_json[FROM]
    to_point = hall_json[TO]
    from_ = to_coord(from_point)
    to = to_coord(to_point)
    waypoints = hall_json[WAYPOINTS]
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
        if level_json[0][TYPE] != LEVEL:
            print('Invalid Args: Type is not level')
            return None
        input_json = level_json[0]
        point = level_json[1]
    except (KeyError, IndexError):
        input_json = level_json
    rooms = input_json[ROOMS]
    hallways = input_json[HALLWAYS]
    objects = input_json[OBJECTS]

    rooms_list = [parse_room_obj(room)[ROOM] for room in rooms]
    halls_list = [parse_hall(hall, rooms_list) for hall in hallways]

    exits = []
    keys = []
    for item in objects:
        posn = item[POS]
        if item[TYPE] == KEY:
            key_coord = to_coord(posn)
            keys.append(Item(KEY, key_coord))
        elif item[TYPE] == EXIT:
            exit_coord = to_coord(posn)
            exits.append(Item(EXIT, exit_coord))

    parsed_level = Level(rooms_list, halls_list, keys, exits)
    return {LEVEL: parsed_level, COORD: to_coord(point) if point else None}   

def parse_actor(actor_input):
    actor_type = actor_input[TYPE]
    name = actor_input[NAME]
    coord = to_coord(actor_input[POS])
    if actor_type == PLAYER:
        return PlayerActor(name, coord)
    else:
        return AdversaryActor(name, type_=actor_type, pos=coord)

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
        if state_json[0][TYPE] != STATE:
            print('Invalid Args: Type is not state')
            return None
        input_json = state_json[0]
        name = state_json[1]
        coord = to_coord(state_json[2])
    except (KeyError, IndexError):
        input_json = state_json

    level_input = input_json[LEVEL]
    players_input = input_json[PLAYERS]
    adversaries_input = input_json[ADVERSARIES]
    exit_locked = input_json[EXIT_LOCKED]

    level = parse_level(level_input)[LEVEL]
    players = [parse_actor(actor_input) for actor_input in players_input]
    adversaries = [parse_actor(actor_input) for actor_input in adversaries_input]
    state = GameState(level, players, adversaries, exit_locked)
    return {STATE: state, NAME: name if name else None, COORD: coord if coord else None}

def parse_manager(game_input):
    try:
        game_json = json.loads(str(game_input))
    except TypeError:
        game_json = game_input
    names = []
    level = None
    max_turns = None
    initial_coords = []
    move_list = []
    
    try:
        names = game_json[0]
        level = parse_level(game_json[1])[LEVEL]
        max_turns = game_json[2]
        initial_coords = [to_coord(point) for point in game_json[3]]
        moves_list = game_json[4]
    except (KeyError, IndexError):
        print('Invalid Args:')
        return None
    
    players = []
    adversaries = [] 
    
    for ii in range(len(initial_coords)):
        if ii < len(names):
            players.append(PlayerActor(names[ii], initial_coords[ii]))
        else:
            adversaries.append(AdversaryActor('adv: ' + str(ii), initial_coords[ii]))

    gm = GameManager()
    gm.register_players(players)
    gm.register_adversaries(adversaries)
    #Initialize dictionary with key = player names to use as a hashmap of moves
    moves_map = dict.fromkeys(names)

    for ii in range(len(players)):
        try:
            moves_map[players[ii].name] = moves_list[ii]
        except IndexError:
        # ??? other exceptions ???
            return None
    return {MANAGER: gm, LEVEL: level, MAX_TURNS: max_turns, MOVES: moves_map}

def parse_levels(levels_input):
    parsed_input = []
    for x in streaming_iterload(levels_input):
        parsed_input.append(x)

    no_levels = int(parsed_input[0])
    parsed_levels = []
    for ii in range(1, no_levels + 1):
        parsed_level = parse_level(parsed_input[ii])[LEVEL]
        parsed_levels.append(parsed_level)

    return parsed_levels

def parse_move(move_input):
    try:
        move = json.loads(move_input)
    except TypeError:
        move = move_input
    move_pos = None
    if move[TYPE] == 'move':
        if move[TO] != 'null':
            move_pos = to_point(move[TO])
    return move_pos
