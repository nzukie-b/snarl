#!/usr/bin/env python

import sys, os

currentdir = os.path.dirname(os.path.realpath(__file__))
tests_dir = os.path.dirname(currentdir)
snarl_dir = os.path.dirname(tests_dir)
src_dir = snarl_dir + '/src'
sys.path.append(src_dir)
from utilities import to_point
from controller.controller import parse_state
from model.gamestate import GameState, State_Obj


def main():
    state_input = sys.stdin.read().strip()
    parsed_input = parse_state(state_input)
    state = parsed_input['state']
    name = parsed_input['name']
    coord = parsed_input['coord']
    level = state.level
    player_names = [player.name for player in state.players]
    if name not in player_names:
        print('[ "Failure", "Player ", {}, " is not a part of the game." ]'.format(name))
        return None
    player = next(player for player in state.players if player.name == name)
    for adv in state.adversaries:
        if adv.pos == coord:
            state.players.remove(player)
            state_obj = State_Obj(state.level, state.players, state.adversaries, state.exit_locked)
            print('[ "Success", "Player ", {}, " was ejected.", {} ]'.format(player.name, state_obj))
            return state_obj
    info = level.info_at_coord(coord)
    if info.traversable:
        if info.object == 'exit' and state.exit_unlocked:
            state.players.remove(player)
            state_obj = State_Obj(state.level, state.players, state.adversaries, state.exit_locked)
            print('[ "Success", "Player ", {}, " exited.", {} ]'.format(name, state_obj))
            return state_obj
        else:
            state.players.remove(player)
            player.pos == coord
            state.players.append(player)
            state_obj = State_Obj(state.level, state.players, state.adversaries, state.exit_locked)
            print('[ "Success", {} ]'.format(state_obj))
            return state_obj
    else:
        print('[ "Failure", "The destination position ", {}, " is invalid." ]'.format(to_point(coord)))
        return None

if __name__ == '__main__':
    main()
