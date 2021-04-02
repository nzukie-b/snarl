#!/usr/bin/env python
import sys, os, argparse, json, math
from constants import GHOST, ZOMBIE

currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
src_dir = snarl_dir + '/src'
sys.path.append(src_dir)
from game.gameManager import GameManager
from controller.controller import parse_levels


parser = argparse.ArgumentParser()
parser.add_argument('-l', '--levels', dest='levels', action='store', default='snarl.levels',
                    help="Location of local levels file")
parser.add_argument('-p', '--players', dest='players', action='store', type=int, default=1,
                    help='Number of players')
parser.add_argument('-s', '--start', dest='start', action='store', type=int, default=1, help='Start level. Not 0 indexed')
parser.add_argument('-o', '--observe', dest='observe', action='store_true', default=False, help='Whether to return observer view of the ongoing game.')



def main(args):
    levels_file = open(args.levels, 'r')
    levels_input = levels_file.read()
    levels = parse_levels(levels_input)
    
    gm = GameManager()
    start_level = args.start - 1


    for ii in range(args.players):
        name = input('Please enter a username for player number {}\n', ii+1)
        gm.register_player(name)

    num_zombies = math.floor(len(levels) / 2) + 1
    num_ghosts = math.floor((len(levels) - 1) / 2)
    for ii in range(num_zombies):
        gm.register_adversary('zombie: {}'.format(ii), ZOMBIE)
    for ii in range(num_ghosts):
        gm.register_adversary('ghost: {}'.format(ii), GHOST)
    
    gm.start_game(levels, start_level=start_level)
    


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
