#!/usr/bin/env python
import sys, os, argparse, json, math
from pathlib import Path
from json.decoder import WHITESPACE
import io
import re

currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
src_dir = snarl_dir + '/src'
sys.path.append(src_dir)
from constants import GHOST, ZOMBIE, P_UPDATE, ROOM, TYPE, P_WIN, KEY
from game.gameManager import GameManager
from controller.controller import parse_levels, to_layout
from utilities import to_coord, coord_radius, to_point, check_position
from common.actorUpdate import ActorUpdate
from game.ruleChecker import RuleChecker
from model.item import Item


parser = argparse.ArgumentParser()
parser.add_argument('-l', '--levels', dest='levels', action='store', default='snarl.levels',
                    help="Location of local levels file")
parser.add_argument('-p', '--players', dest='players', action='store', type=int, default=1,
                    help='Number of players')
parser.add_argument('-s', '--start', dest='start', action='store', type=int, default=1, help='Start level. Not 0 indexed')
parser.add_argument('-o', '--observe', dest='observe', action='store_true', default=False, help='Whether to return observer view of the ongoing game.')

# Wasn't able to find a python library to easily handle stream json values
# The following code block draws from a stack overflow post to handle stream json values (https://stackoverflow.com/questions/6886283/how-i-can-i-lazily-read-multiple-json-values-from-a-file-stream-in-python)

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


def main(args):
    levels_file = open(args.levels, 'r')
    levels_input = Path(args.levels).read_text()
    temp_levels = []
    for x in streaming_iterload(levels_input):
        #if not isinstance(x, int):
            #    str(x.replace('\'', '\"'))
        temp_levels.append(json.dumps(x))

    print(temp_levels)
    levels = parse_levels(temp_levels)
    
    gm = GameManager()
    start_level = args.start - 1


    for ii in range(args.players):
        name = input('Please enter a username for player number {}\n'.format(ii+1))
        gm.register_player(name)

    num_zombies = math.floor(len(levels) / 2) + 1
    num_ghosts = math.floor((len(levels) - 1) / 2)
    for ii in range(num_zombies):
        gm.register_adversary('zombie: {}'.format(ii), ZOMBIE)
    for ii in range(num_ghosts):
        gm.register_adversary('ghost: {}'.format(ii), GHOST)
    
    gm.start_game(levels, start_level=start_level)

    while True:
        for index_in_players in range(0, len(gm.players)):
            player = gm.players[index_in_players]
            invalid_input = True
            while invalid_input:
                move_player_loc = input('[Current Player\'s turn: {}] Type in location you want to move to (Type into format ' 
                                        '\"\'row number\', \'col number\'\""\n'.format(player.name))
                move_player_loc = [int(x) for x in move_player_loc.split(', ')]
                print(move_player_loc)
                if len(move_player_loc) != 2:
                    print("INVALID LOCATION INPUT")
                else:
                    player.move_to_tile(to_coord(move_player_loc), gm)
                    if player.name in gm.gamestate.out_players:
                        print("Player " + player.name + " was expelled")
                    if player.name in exited_players:
                        print("Player " + player.name + " exit")
                    invalid_input = False

            new_player_loc = to_coord(move_player_loc)

            player_object = gm.get_player_actor(player.name)

            update = ActorUpdate(new_player_loc)
            update.position = new_player_loc
            update.type = P_UPDATE
            view_dimensions = to_coord([(player_object.move_speed * 2) + 1, (player_object.move_speed * 2) + 1])
            update.layout = to_layout(new_player_loc, gm.gamestate.current_level, view_dimensions)
            update.layout_coords = coord_radius(new_player_loc, view_dimensions)

            actors = []
            other_players = [p for p in gm.players if p.name is not name]
            for player in other_players:
                player_obj = gm.get_player_actor(player.name)
                if player_obj.pos in update.layout_coords:
                    actors.append({"type": 'player', "name": player_obj.name, "position": to_point(player_obj.pos)})
            for adv in gm.adversaries:
                adversary_obj = gm.get_adversary_actor(adv.name)
                if adversary_obj.pos in update.layout_coords:
                    actors.append({"type": 'ghost', "name": adversary_obj.name, "position": to_point(adversary_obj.pos)})
            level = gm.gamestate.current_level
            pos_info = check_position(player.pos, level)

            is_room = pos_info[TYPE] == ROOM
            objects = []
            if is_room:
                for room in level.rooms:
                    for item in room.items:
                        if item.pos in update.layout_coords:
                            objects.append({"type": 'key', "position": to_point(item)})
            for exit_ in level.exits:
                if exit_ in update.layout_coords:
                    objects.append({"type": 'exit', "position": to_point(exit_)})

            update.actors = actors
            update.objects = objects

            player.recieve_update(update)

            item = Item(KEY, player.pos)

            if RuleChecker.validate_item_interaction(player_object, item):
                print("Player " + player.name + " found the " + item.type)

            if RuleChecker.is_game_over(gm.gamestate):
                print("GAME OVER, exited successfully {} times and found {} keys")
                exit()

            is_last_level = False
            current_level = gm.gamestate.current_level
            if RuleChecker.is_level_over(gm.gamestate):
                if is_last_level and gm.game_status == P_WIN:
                    "Congratulations players, you have won!"
                    exit()
                else:
                    "Sorry players, you have lost :'( You failed on level {}".format(current_level)
                    exit()



if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
