#!/usr/bin/env python
import sys, os
import pytest
currentdir = os.path.dirname(os.path.realpath(__file__))
game_dir = os.path.dirname(currentdir)
sys.path.append(game_dir)
from level import Coord, Room, Hallway, Level, Tile, check_room, check_hallway

@pytest.fixture
def setup_room1():
    '''Initializes example Room'''
     #Room 1 example
    tiles = [Coord(7, 6),Coord(7, 8),Coord(7, 9),Coord(7, 10), Coord(6, 6), Coord(6, 8), Coord(8, 9), Coord(8,6), Coord(8, 7), Coord(8,8), Coord(8, 9), Coord(8, 10), Coord(9, 6), Coord(9, 7), Coord(9,8) ]
    start = Coord(5, 5)
    dimensions = Coord(5, 5)
    doors = [Coord(8,10), Coord(7, 10), Coord(6, 10)]
    items = [Coord(6, 6), Coord(7, 8)]
    room = Room(start, dimensions, tiles, doors, items)
    return room

@pytest.fixture
def setup_hallway(setup_room1):
    hall_start = Coord(6, 10)
    hall = Hallway(hall_start, Coord(2, 3), [setup_room1])
    return hall

@pytest.fixture
def setup_room2():
    #Room 2 example
    tiles1 = [Coord(7, 14), Coord(7, 16), Coord(7, 17), Coord(6, 16), Coord(8, 17), Coord(8, 14), 
                Coord(6, 13), Coord(7, 13), Coord(7, 15), Coord(9, 17), Coord(9, 16), Coord(9, 15), Coord (9, 14), Coord(6, 16)]
    start1 = Coord(5, 13)
    dimensions1 = Coord(5, 5)
    doors1 = [Coord(8, 13), Coord(7, 13), Coord(6, 13)]
    items1 = [Coord(8, 14), Coord(7, 17)]
    room2 = Room(start1, dimensions1, tiles1, doors1, items1)
    return room2


def test_test(setup_hallway):
    assert setup_hallway.check_orientation() == True