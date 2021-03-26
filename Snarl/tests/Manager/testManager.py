import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
tests_dir = os.path.dirname(currentdir)
snarl_dir = os.path.dirname(tests_dir)
src_dir = snarl_dir + '/src'
sys.path.append(src_dir)
from game.gameManager import start_game, request_player_move, apply_player_item_interaction
from game.ruleChecker import validate_item_interaction, validate_player_movement

