#!/usr/bin/env python
import sys, os, copy
currentdir = os.path.dirname(os.path.realpath(__file__))
tests_dir = os.path.dirname(currentdir)
snarl_dir = os.path.dirname(tests_dir)
src_dir = snarl_dir + '/src'
sys.path.append(src_dir)
from utilities import to_point
from controller.controller import parse_manager, to_coord
from model.gamestate import State_Obj

def main():
    manager_input = sys.stdin.read().strip()
    parsed_input = parse_manager(manager_input)
    gm = parsed_input['manager']
    max_turns = parsed_input['max_turns']
    moves_map = parsed_input['moves']
    level = parsed_input['level']
    names = [player.name for player in gm.players]
    player_updates = []
    move_update = []
    gm.start_game(level)

    for name in gm.player_turns:
        player = next(player for player in gm.players if player.name == name)
        update = {
            "type": 'player-update',
            "layout": None,
            "position": to_point(player.pos),
            "objects": None,
            "actors": None 
        }
        #processing here 

        player_updates.append([name, update])


    for ii in range(max_turns):
        for name in gm.player_turns:
            err = 0
            player = next(player for player in gm.players if player.name == name)
            player_moves = copy.deepcopy(moves_map[player.name])
            
            while ii + err in range(len(player_moves)):
                try:
                    active_move = player_moves[ii + err]
                except (IndexError, KeyError):
                    #exhausted moves list
                    
                move = moves_map[player.name].remove(active_move)
                if move['to'] == 'null':
                    move_update.append([name, active_move['to'], 'OK'])
                    break
                else:
                    move_coord = to_coord(move['to'])

                move_info = gm.request_player_move(player.name, move_coord)
                adv_coords = [adv.pos for adv in gm.adversaries]
                if move_info is not None:
                    res = 'OK'
                    if move_info.object == 'exit' and gm.gamestate.exit_unlocked:
                        res = 'Exit'
                    elif move_info.object == 'key':
                        res = 'Key'
                    elif move_coord in adv_coords:
                        res = 'Eject'
                    elif move_info.traversable == False:
                        res = 'Invalid'
                    move_update.append([name, move['to'], res])
                    break
                else:
                    err += 1
                    # if err not in range(len(player_moves)):
                        #TODO: Stop and return the result?
                        # return False

if __name__ == '__main__':
    main()
