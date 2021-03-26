#!/usr/bin/env python
import sys, os
import pytest

currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/src'
sys.path.append(game_dir)
from coord import Coord
from utilities import to_coord, to_point
from model.room import Room
from model.hallway import Hallway
from model.level import Level
from model.gamestate import GameState, create_initial_game_state
from model.adversary import Adversary
from model.player import PlayerActor
from game.ruleChecker import RuleChecker
from game.gameManager import GameManager


@pytest.fixture
def room2():
    # Room 2 example
    tiles1 = [Coord(7, 15), Coord(7, 17), Coord(7, 18), Coord(6, 17), Coord(8, 17), Coord(8, 15),
              Coord(6, 15), Coord(7, 15), Coord(7, 15), Coord(9, 17), Coord(9, 16), Coord(9, 15), Coord(9, 15),
              Coord(6, 16)]
    start1 = Coord(5, 15)
    dimensions1 = Coord(5, 5)
    doors1 = [Coord(7, 15)]
    items1 = [Coord(8, 17), Coord(7, 17)]
    room2 = Room(start1, dimensions1, tiles1, doors1, items1)
    return room2


@pytest.fixture
def room3():
    tiles1 = [Coord(7, 1), Coord(7, 2), Coord(7, 3), Coord(7, 18), Coord(6, 4), Coord(6, 1), Coord(6, 3), Coord(7, 5),
              Coord(8, 4), Coord(8, 2), Coord(8, 3), Coord(8, 4), Coord(8, 5), Coord(9, 2), Coord(9, 3), Coord(9, 4)]
    start1 = Coord(5, 0)
    dimensions1 = Coord(5, 5)
    doors1 = [Coord(7, 5)]
    items1 = [Coord(6, 1), Coord(7, 3)]
    room3 = Room(start1, dimensions1, tiles1, doors1, items1)
    return room3


@pytest.fixture
def hallway(room3, room2):
    '''Initializes a Hallway with a vertical orientation'''
    hall = Hallway([Coord(1, 10), Coord(5, 10)], [room3, room2])
    return hall


@pytest.fixture
def level2(room3, room2, hallway):
    level = Level([room3, room2], [hallway], [Coord(7, 1)], [Coord(9, 17)])
    return level


@pytest.fixture
def gamestate1(level2):
    '''Initializes example gamestate'''
    players = []
    adversaries = []
    for i in range(3):
        p = PlayerActor('Bruh ' + str(i))
        p.health = 3
        players.append(p)
        a = Adversary('Evil Bruh ' + str(i))
        a.health = 3
        adversaries.append(a)

    gs_info = create_initial_game_state(level2, players, adversaries)
    gamestate = GameState(level2, gs_info[0], gs_info[1])
    return gamestate


def test_gamemanager(level2):
    gm = GameManager()
    player_names = []
    for i in range(3):
        player_names.append("bruh " + str(i))
    gm.register_player_names(player_names)
    assert len(gm.players) == 3
    assert gm.players[0].name == "bruh 0"
    assert gm.players[1].name == "bruh 1"
    assert gm.players[2].name == "bruh 2"
    gm.start_game(level2)
    rc = RuleChecker()
    assert rc.validate_player_movement(Coord(8, 2), Coord(8, 3), level2)
    assert rc.validate_player_movement(Coord(8, 2), Coord(8, 4), level2)
    assert not rc.validate_player_movement(Coord(8, 2), Coord(7, 4), level2)['info'].traversable
    assert not rc.validate_player_movement(Coord(8, 2), Coord(112, 10), level2)['info'].traversable
    assert not rc.validate_player_movement(Coord(8, 2), Coord(10, 2), level2)['info'].traversable
    gm.apply_player_item_interaction(gm.gamestate.players[2], Coord(8, 17))
    assert rc.validate_item_interaction(gm.gamestate.players[2], Coord(8, 3), level2)