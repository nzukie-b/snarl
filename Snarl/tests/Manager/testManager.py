#!/usr/bin/env python
import sys, os, copy
currentdir = os.path.dirname(os.path.realpath(__file__))
tests_dir = os.path.dirname(currentdir)
snarl_dir = os.path.dirname(tests_dir)
src_dir = snarl_dir + '/src'
sys.path.append(src_dir)
from coord import Coord
from constants import ROOM, HALL
from utilities import check_position, to_point, to_coord, coord_radius
from controller.controller import parse_manager, to_layout
from model.gamestate import State_Obj

def main():
    manager_input = sys.stdin.read().strip()
    parsed_input = parse_manager(manager_input)
    gm = parsed_input['manager']
    max_turns = parsed_input['max_turns']
    moves_map = parsed_input['moves']
    level = parsed_input['level']
    names = [player_name for player_name in gm.players_turns]
    player_updates = []
    move_update = []
    manager_updates = []
    gm.start_game(level)

    ## Initial player  updates ##
    for name in names:
        player = next(player for player in gm.players if player.name == name)
        update = {
            "type": 'player-update',
            "layout": None,
            "position": to_point(player.pos),
            "objects": None,
            "actors": None 
        }
        #processing here 
        view_radius = Coord(5, 5)
        coords = coord_radius(player.pos, view_radius)
        objects = []
        actors = []
        other_players = [p for p in gm.players if p.name is not name]
        for player in other_players:
            if player.pos in coord:
                actors.append({"type": 'player', "name": player.name, "position": to_point(player.pos)})
        for adv in gm.adversaries:
            if adv.pos in coord:
                actors.append({"type": 'zombie', "name": adv.name, "posision": to_point(adv.pos)})
        level = gm.gamestate.level
        pos_info = check_position(player.pos, level)
        is_room = pos_info['type'] == ROOM
        origin = pos_info['origin']
        if is_room:
            for room in level.rooms:
                for item in room.items:
                    if item in coords:
                        objects.append({"type": 'key', "position": to_point(item)})
        for exit_ in level.exits:
            if exit_ in coords:
                objects.append({"type": 'exit', "position": to_point(exit_)})
        layout = to_layout(player.pos, level, view_radius)
        update['layout'] = layout
        update['objects'] = objects
        update['actors'] = actors
        data = [name, update]
        player_updates.append(data)
        manager_updates.append(data)

    ## Move Updates ##
    #NOTE Turn starts at 0
    for turn in range(max_turns):
        for name in names:
            err = 0
            player = next(player for player in gm.players if player.name == name)
            # Copy the moves map, and use this copy for iteration
            player_moves = copy.deepcopy(moves_map[player.name])
            
            while err in range(len(player_moves)):
                try:
                    active_move = player_moves[turn + err]
                    # Cases where player_moves[turn] is an invalid index, such as turn 2 (3rd turn when incl. 0) when only 2 moves, are handled below
                except (IndexError):
                    #Move list exhausted / More turns than moves
                    state_obj = State_Obj(gm.gamestate.level, gm.gamestate.players, gm.gamestate.adversaries, gm.exit_locked)
                    print('[{}, {}]'.format(state_obj, manager_updates))
                    return manager_updates

                if active_move['to'] == 'null':
                    gm.request_player_move(player.name, player.pos)
                    data = [name, active_move, 'OK']
                    move_update.append(data)
                    manager_updates.append(data)
                    break
                else:
                    move_coord = to_coord(active_move['to'])

                move_info = gm.request_player_move(player.name, move_coord)
                valid_move = move_info['valid_move']
                info = move_info['info']
                adv_coords = [adv.pos for adv in gm.adversaries]

                if move_info is not None:
                    #Valid player turn
                    res = 'OK'
                    if info.traversable == False or valid_move == False:
                        # Remove invalid moves from the original moves_map so that the next time moves_map is copied, previous invalid moves will not be included.
                        #   This should help preserve turn order as all next moves should start at the same index since any invalid before that will have been removed
                        move = moves_map[player.name].remove(active_move)
                        err += 1
                        res = 'Invalid'
                        data = [name, move, res]
                        move_update.append(data)
                        manager_updates.append(data)
                        #Continue while loop until a valid move is reached or the move list is exhausted
                        continue
                    
                    elif move_info.object == 'exit' and gm.gamestate.exit_unlocked:
                        res = 'Exit'
                        move_update.append(data)
                        manager_updates.append(data)
                        state_obj = State_Obj(gm.gamestate.level, gm.gamestate.players, gm.gamestate.adversaries, gm.exit_locked)
                        print('[{}, {}]'.format(state_obj, manager_updates))
                        return manager_updates
                    elif move_info.object == 'key':
                        res = 'Key'
                    elif move_coord in adv_coords:
                        res = 'Eject'
                    data = [name, active_move, res]
                    move_update.append(data)
                    manager_updates.append(data)
                    break
                else:
                    print('Invalid Turn ??')
                        #TODO: Stop and return the result?

    state_obj = State_Obj(gm.gamestate.level, gm.gamestate.players, gm.gamestate.adversaries, gm.exit_locked)
    print('[{}, {}]'.format(state_obj, manager_updates))
    return manager_updates


if __name__ == '__main__':
    main()
