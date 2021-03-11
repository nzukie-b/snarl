#!/usr/bin/env python
import sys, os
import pytest
currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/src'
sys.path.append(game_dir)
from coord import Coord
from model.room import Room
from model.hallway import Hallway
from model.level import Level
from model.gamestate import GameState, create_initial_game_state
from utilities import check_level


#Room 1 example
tiles = [Coord(7, 6),Coord(7, 8),Coord(7, 9),Coord(7, 10), Coord(6, 6), Coord(6, 8), Coord(8, 9), Coord(8,6), Coord(8, 7), Coord(8,8), Coord(8, 9), Coord(8, 10), Coord(9, 6), Coord(9, 7), Coord(9,8), Coord(6, 10)]
start = Coord(5, 0)
dimensions = Coord(5, 5)
doors = [Coord(7, 10)]
items = [Coord(6, 6), Coord(7, 8)]

@pytest.fixture
def room1():
    '''Initializes example Room'''
    room = Room(start, dimensions, tiles, doors, items)
    return room

@pytest.fixture
def room2():
    #Room 2 example
    tiles1 = [Coord(7, 15), Coord(7, 17), Coord(7, 18), Coord(6, 17), Coord(8, 17), Coord(8, 15), 
                Coord(6, 15), Coord(7, 15), Coord(7, 15), Coord(9, 17), Coord(9, 16), Coord(9, 15), Coord (9, 15), Coord(6, 16)]
    start1 = Coord(5, 15)
    dimensions1 = Coord(5, 5)
    doors1 = [Coord(7, 15)]
    items1 = [Coord(8, 17), Coord(7, 17)]
    room2 = Room(start1, dimensions1, tiles1, doors1, items1)
    return room2

@pytest.fixture
def room3():
    tiles1 = [Coord(7, 1), Coord(7, 2), Coord(7, 3), Coord(6, 5), Coord(6, 4), Coord(6, 1), Coord(6, 3), Coord(7, 5), 
                Coord(8, 4), Coord(8, 2), Coord(8, 3), Coord(8, 4), Coord(8, 5), Coord(9, 2), Coord (9, 3), Coord(9, 4)]
    start1 = Coord(5, 0)
    dimensions1 = Coord(5, 5)
    doors1 = [Coord(7, 5)]
    items1 = [Coord(6, 1), Coord(7, 3)]
    room3 = Room(start1, dimensions1, tiles1, doors1, items1)
    return room3


@pytest.fixture
def hallway(room1, room2):
    '''Initializes a Hallway with a vertical orientation'''
    hall = Hallway([Coord(1, 10), Coord(5, 10)], [room1, room2])
    return hall

@pytest.fixture 
def horizontal_hallway():
    '''Initializes a Hallway with a horizontal orientation'''
    #hall_start = Coord(0, 0)
    hall_start = Coord(4, 3)
    hall = Hallway([hall_start, Coord(4, 5)], [Room(start, dimensions, [Coord(5, 3)], [Coord(5, 3)])])
    return hall

@pytest.fixture
def invalid_hallway():
    '''Initializes an invalid Hallway'''
    hall_start = Coord(0, 0)
    hall = Hallway([hall_start, Coord(5, 5)], [Room(start, dimensions, [Coord(5, 5)], [Coord(3, 3)])])
    return hall

@pytest.fixture
def level1(room1, room2, hallway):
    '''Initializes example Level'''
    level = Level([room1, room2], [hallway], [Coord(8, 9)], [Coord(9, 15)])
    return level

@pytest.fixture
def level2(room3, room2, hallway):
    level = Level([room3, room2], [hallway], [Coord(7, 1)], [Coord(9, 17)])
    return level

@pytest.fixture
def gamestate1(level1):
    '''Initializes example gamestate'''
    gs_info = create_initial_game_state(level1, 3, 3)
    gamestate = GameState(gs_info[0], gs_info[1])
    return gamestate

## TESTS START HERE ##

def test_coord():
    c1 = Coord(0, 0)
    c2 = Coord(0, 1)
    c3 = Coord(0, 0)
    assert c1 != c2
    assert c2 != c3
    assert c1 == c3

def test_valid_level(level1):
    assert check_level(level1) == True

def test_invalid_level_rooms(capsys, room1, hallway):
    room2 = Room(start, dimensions, tiles, doors)
    level = Level([room1, room2], [hallway])
    valid_level = check_level(level)
    capture = capsys.readouterr()
    assert capture.out == 'Invalid Level: Duplicate rooms\n'
    assert valid_level == False


def test_invalid_level_hallway(capsys, room1, hallway):
    hall2 = Hallway(hallway.doors, [room1])
    level = Level([room1], [hallway, hall2])
    valid_level = check_level(level)
    capture = capsys.readouterr()
    assert capture.out == 'Invalid Level: Duplicate hallways\n'
    assert valid_level == False


def test_invalid_level_shared_coords(capsys, room1, level1):
    hall = Hallway([Coord(5, 15), Coord(10, 20)], [room1, room2])
    level1.hallways[0] = hall
    valid_level = check_level(level1)
    capture = capsys.readouterr() 
    # assert capture.out == 'Invalid Level: Hallway or Room sharing coordinates\n'
    # TODO: Fix hallway to be valid
    assert valid_level == False


def test_invalid_level_dimensions(capsys, level1):
    invalid_dimensions = Room(Coord(6, 1), Coord(6, 6), tiles, doors)
    level1.rooms.append(invalid_dimensions)
    valid_level = check_level(level1)
    capture = capsys.readouterr()
    assert capture.out == 'Invalid Level: Overlapping Room(s) or Hallway(s)\n'
    assert valid_level == False
    

def test_info_at_coord(level2):
    coord = Coord(7, 1)
    coord_info = level2.info_at_coord(coord)
    assert coord_info.traversable == True
    assert coord_info.object == 'key'
    assert coord_info.type == 'room'
    assert len(coord_info.reachable) == 0
    coord2 = Coord(9, 17)
    coord_info = level2.info_at_coord(coord2)
    assert coord_info.traversable == True
    assert coord_info.object == 'exit'
    assert coord_info.type == 'room'
    assert len(coord_info.reachable) == 0
    coord3 = Coord(0, 0)
    coord_info = level2.info_at_coord(coord3)
    assert coord_info.traversable == False
    assert coord_info.object == 'null'
    assert coord_info.type == 'void'
    assert len(coord_info.reachable) == 0
