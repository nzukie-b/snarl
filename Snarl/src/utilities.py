#!/usr/bin/env python
import io, re, json
from json.decoder import WHITESPACE
import socket
from common.player import Player
from coord import Coord
from constants import EXIT, HALLWAY, KEY, LAYOUT, ORIGIN, PLAYER, POS, P_UPDATE, ROOM, TYPE
import random
from remote.messages import ActorPosition, ObjectPos, RemoteActorUpdate

def check_hallway(hallway):
    '''Checks that a hallway is valid by checking that the hallway's orientation is either vertical or horizontal.'''
    try:
        hallway.check_orientation()
        return True
    except Exception as err:
        return False


# Since valid_doors is only checked after valid_tiles is True it is not an issue that check_doors does not guarantee that the walkable tiles are inside the room as check_tiles handles guarantees that 
def check_room(room):
    '''Checks that the provided room is valid by checking the tiles and doors of the provided room'''
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
def check_dimensions(x_dimensions, y_dimensions, level_dimensions):
    '''Checks that the provided coordinates, are within the level dimensions. 
        If so, returns the origin of the room/hallway overlapping the point. If the provided coordinates are not within the level returns None'''
    row_start = x_dimensions[0]
    row_end = x_dimensions[1]
    col_start = y_dimensions[0]
    col_end = y_dimensions[1]
    for level in level_dimensions:
        # level_dimensions list of tuples in format ((x_origin, x_origin+dest), (y_origin, y_origin+dest)), Created in check_level_dimensions
        level_row_origin = level[0][0]
        level_row_dest = level[0][1]
        level_col_origin = level[1][0]
        level_col_dest = level[1][1]
        for row in range(row_start, row_end + 1):
            for col in range(col_start, col_end + 1):
                # print(x,y)
                if row in range(level_row_origin, level_row_dest + 1) and col in range(level_col_origin, level_col_dest + 1):
                    return Coord(level_row_origin, level_col_origin)
    return False

def check_level(level):
    '''Checks that the provided level is valid'''
    for room in level.rooms:
        if check_room(room) == False:
            #print("ROOM CHECK FAILED")
            return False
    for hall in level.hallways:
            if check_hallway(hall) == False:
                return False
    #print("dimension check: " + str(level.check_level_dimensions()))
    return level.check_level_dimensions()

def get_reachable_tiles(coord, walkable_tiles):
    '''Takes in a list of walkable tiles, and returns a list of tiles reachable within a 1 space move'''
    tiles = []
    for tile in walkable_tiles:
        #TODO: Separate this into some coord comparison function?
        if (tile.row == coord.row) and (tile.col ==  coord.col + 1 or tile.col == coord.col - 1):
            tiles.append(tile)
        elif (tile.col == coord.col) and (tile.row == coord.row + 1 or tile.row == coord.row - 1):
            tiles.append(tile)
    return tiles


def to_coord(point):
    '''Converts the point coordinate system i.e. [0, 0] to a Coord object {row: 0, col:0}'''
    if isinstance(point, Coord):
        # if point is already a Coord object return it.
        return point
    else:
        return Coord(point[0], point[1])

def to_point(coord):
    '''Converts a Coord object to the points coordinate system'''
    if isinstance(coord, Coord):
        return [coord.row, coord.col]
    else:
        return coord


def get_reachable_rooms(origin, level):
    '''Returns a list of coords specifying the origin of rooms reachable through 1 hallway from room at the provided coordinate. Returns None if the provided coordinate does not match the origin of a room'''
    reachable = []
    for room in level.rooms:
        if origin == room.origin:
            for door in room.doors:
                for hall in level.hallways:
                    if door in hall.doors:
                        reachable += [room.origin for room in hall.rooms if door not in room.doors]
    return reachable

def get_reachable_halls(origin, level):
    '''Returns a list of coords specifying the origin of rooms that are connected through the hallway at the provided coordinate. Returns None if the provided coordinate does not match the origin of a hallway'''
    reachable = []
    for hall in level.hallways:
        if origin == hall.origin:
            reachable += [room.origin for room in hall.rooms]
    return reachable


def check_position(pos, level):
    '''Checks if the provide point is inside the level. If so returns whether it is a hallway or a room, and its respective origin.'''
    row_dimensions = (pos.row, pos.row)
    col_dimensions = (pos.col, pos.col)
    room_dimensions = level.get_level_room_dimensions()
    hall_dimensions = level.get_level_hallway_dimensions()
    pos = None
    # Room or Hallway
    origin_type = None
    room_origin = check_dimensions(row_dimensions, col_dimensions, room_dimensions)
    hall_origin = check_dimensions(row_dimensions, col_dimensions, hall_dimensions)
    if room_origin:
        origin_type = ROOM
        pos = room_origin
    elif hall_origin:
        origin_type = HALLWAY
        pos = hall_origin
    return {TYPE: origin_type, ORIGIN: pos}


def coord_radius(pos, dimensions) -> set:
    '''Returns a set of coordinates the provided coordinate is at the center'''
    coords = set()
    for ii in range(1, int(round(dimensions.row/2)) + 1):
        for jj in range(1, int(round(dimensions.col/2)) + 1):
            c1 = Coord(pos.row + ii, pos.col + jj)
            c2 = Coord(pos.row + ii, pos.col - jj)
            c3 = Coord(pos.row - ii, pos.col + jj)
            c4 = Coord(pos.row - ii, pos.col - jj)
            c5 = Coord(pos.row, pos.col + jj)
            c6 = Coord(pos.row, pos.col - jj)
            c7 = Coord(pos.row + ii, pos.col)
            c8 = Coord(pos.row - ii, pos.col)
            coords.update([c1, c2, c3, c4, c5, c6, c7, c8])
    return list(coords)

# def update_player(current_player: Player, other_player: Player):
#     if isinstance(other_player, Player) and isinstance(current_player, Player):
#         if current_player.player_obj.pos in other_player.visible_tiles:
#             other_player.actors.append(MoveUpdate(P_UPDATE, current_player.name, to_coord(current_player.player_obj.pos)))

# def update_players(current_player: Player, other_players: Player):
#     other_players = [player for player in other_players if player.name != current_player.name]
#     for other in other_players:
#         update_player(current_player, other)


def update_remote_player(player: Player, gm):
        player_obj = gm.get_player_actor(player.name)
        update = RemoteActorUpdate()
        update.position = player_obj.pos
        update.type = P_UPDATE
        view_dimensions = [(player_obj.move_speed * 2) + 1, (player_obj.move_speed * 2) + 1]
        layout = to_layout(player_obj.pos, gm.gamestate.current_level, view_dimensions) 
        update.layout = layout[LAYOUT]
        update.layout_coords = coord_radius(player_obj.pos, to_coord(view_dimensions))

        actors = []
        other_players = [p for p in gm.players if p.name is not player.name]
        for player in other_players:
            player_obj = gm.get_player_actor(player.name)
            if player_obj.pos in update.layout_coords:
                actor_type = PLAYER
                actor_name = player_obj.name
                pos = to_point(player_obj.pos)
                actor_pos = ActorPosition(actor_type, actor_name, pos)
                actors.append(actor_pos)      
        for adv in gm.adversaries:
            adversary_obj = gm.get_adversary_actor(adv.name)
            if adversary_obj.pos in update.layout_coords:
                actor_type = adversary_obj.type
                actor_name = adversary_obj.name
                pos = to_point(adversary_obj.pos)
                actor_pos = ActorPosition(actor_type, actor_name, pos)
                actors.append(actor_pos)
        level = gm.gamestate.current_level
        pos_info = check_position(player_obj.pos, level)

        is_room = pos_info[TYPE] == ROOM
        objects = []
        if is_room:
            for room in level.rooms:
                for item in room.items:
                    if item.pos in update.layout_coords:
                        obj_pos = ObjectPos(KEY, to_point(item.pos))
                        objects.append(obj_pos)
        for exit_ in level.exits:
            if exit_ in update.layout_coords:
                obj_pos = ObjectPos(EXIT, to_point(exit_))
                objects.append(obj_pos)
        update.actors = actors
        update.objects = objects
        player.recieve_update(update)

def update_remote_players(players, gm):
    for player in players:
        update_remote_player(player, gm)


def update_adversary_players(adversaries, player_coords):
    for adv in adversaries:
        adv.update_player_coords(player_coords)

def update_adversary_levels(adversaries, cur_level):
    for adv in adversaries:
        adv.update_current_level(cur_level)
    
def get_random_room_coord(level) -> Coord:
    '''Returns a random walkable coord in a room'''
    room = random.choice(level.rooms)
    tile = random.choice(room.tiles)
    return tile

def get_closest_coord(cur_pos, target):
    temp_rows = [cur_pos.row + 1, cur_pos.row, cur_pos.row - 1]
    temp_cols = [cur_pos.col + 1, cur_pos.col, cur_pos.col - 1]
    min_row = lambda row_val: abs(row_val - target.row)
    min_col = lambda col_val: abs(col_val - target.col)
    move_row = min(temp_rows, min_row)
    move_col = min(temp_cols, min_col) if move_row == cur_pos.row else cur_pos.col 
    move = Coord(move_row, move_col)
    return move

def get_cardinal_coords(cur_pos):
    up = Coord(cur_pos.row - 1, cur_pos.col)
    down = Coord(cur_pos.row + 1, cur_pos.col)
    left = Coord(cur_pos.row, cur_pos.col - 1)
    right = Coord(cur_pos.row, cur_pos.col + 1)
    directions = [up, down, left, right]
    return directions

def find_room_by_origin(origin: Coord, level):
    for room in level.rooms:
        if room.origin == origin:
            return room

def find_hallway_by_origin(origin: Coord, level):
    for hall in level.hallways:
        if hall.origin == origin:
            return hall

def to_layout(pos, level, dimensions):
    '''Takes a level and returns a layout of tiles centered around the provided point'''
    pos_info = check_position(pos, level)
    origin = pos_info['origin']
    is_room = pos_info[TYPE] == ROOM
    #print("DIM: " + str(dimensions))
    dimensions = to_coord(dimensions)
    layout = [[0 for ii in range(dimensions.row)] for jj in range(dimensions.col)]
    coords = coord_radius(pos, dimensions)

    if pos_info[TYPE] == ROOM:
        room = next(room for room in level.rooms if room.origin == origin)
        for tile in room.tiles:
            if tile in coords:
                #origin 5, 5 
                try:
                    layout[tile.row - origin.row][tile.col - origin.col] = 1
                except IndexError:
                    pass
        for door in room.doors:
            if door in coords:
                layout[door.row - origin.row][door.col - origin.col] = 2
    elif pos_info[TYPE] == HALLWAY:
        hall = next(hall for hall in level.hallways if hall.origin == origin)
        for ii in range(hall.origin.row, hall.origin.row + hall.dimensions.row + 1):
            for jj in range(hall.origin.col, hall.origin.col + hall.dimensions.col + 1):
                hall_coord = Coord(ii, jj)
                if hall_coord in coords:
                    try:
                        layout[hall_coord.row - origin.row][hall_coord.col - origin.col] = 1
                    except IndexError:
                        pass
        for door in hall.doors:
            if door in coords:
                layout[door.row - origin.row][door.col - origin.col] = 2
    return {POS: pos, LAYOUT: layout}


def send_msg(sock: socket.SocketType, msg: str, to: str):
    sock.sendall(msg.encode('utf-8'))
    if isinstance(msg, dict):
        print(to, '<<', msg.__dict__)
    else:
        print(to, '<<', msg.replace('\\', ''))


def receive_msg(sock: socket.SocketType, from_: str):
    data = sock.recv(4096)
    if not data:
        return data
    res = data.decode('utf-8')
    if isinstance(res, dict):
        print(from_, '>>', res.__dict__)
    else:
        print(from_, '>>', res.replace('\\', ''))
    return res
# CODE BLOCK FROM STACK OVERFLOW #

braces = '{}[]'
whitespace_esc = ' \t'
braces_esc = '\\'+'\\'.join(braces)
balance_map = dict(zip(braces, [1, -1, 1, -1]))
braces_pat = '['+braces_esc+']'
no_braces_pat = '[^'+braces_esc+']*'
exited_players = []
until_braces_pat = no_braces_pat+braces_pat


def streaming_find_iter(pat, stream):
    for s in stream:
        while True:
            match = re.search(pat, s)
            if not match:
                yield (False, s)
                break
            yield (True, match.group())
            s = re.split(pat, s, 1)[1]

def simple_or_compound_objs(stream):
    obj = ''
    unbalanced = 0
    for (c, m) in streaming_find_iter(re.compile(until_braces_pat), stream):
        if (c == 0):  # no match
            if (unbalanced == 0):
                yield (0, m)
            else:
                obj += m
        if (c == 1):  # match found
            if (unbalanced == 0):
                yield (0, m[:-1])
                obj += m[-1]
            else:
                obj += m
            unbalanced += balance_map[m[-1]]
            if (unbalanced == 0):
                yield (1, obj)
                obj = ""

def iterload(fp, cls=json.JSONDecoder, **kwargs):
    if (isinstance(fp, io.TextIOBase) or isinstance(fp, io.BufferedIOBase) or
            isinstance(fp, io.RawIOBase) or isinstance(fp, io.IOBase)):
        string = fp.read()
    else:
        string = str(fp)

    decoder = cls(**kwargs)
    idx = WHITESPACE.match(string, 0).end()
    while idx < len(string):
        obj, end = decoder.raw_decode(string, idx)
        yield obj
        idx = WHITESPACE.match(string, end).end()

def streaming_iterload(stream):
    for c, o in simple_or_compound_objs(stream):
        for x in iterload(o):
            yield x

# END OF STACK OVERFLOW CODE BLOCK