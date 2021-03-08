#!/usr/bin/env python

import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
tests_dir = os.path.dirname(currentdir)
snarl_dir = os.path.dirname(tests_dir)
src_dir = snarl_dir + '/src'
sys.path.append(src_dir)
from controller.controller import parse_state
from model.gamestate import GameState

if __name__ == '__main__':
    state_input = sys.stdin.read().strip()
    parsed_input = parse_state(state_input)
    state = parsed_input['state']
    name = parsed_input['name']
    coord = parsed_input['coord']
