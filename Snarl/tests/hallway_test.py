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
from utilities import check_hallway


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

def test_check_hallway(hallway):
    assert check_hallway(hallway) == True


def test_hallway_orientation(hallway, horizontal_hallway):
    assert hallway.check_orientation() == False
    assert horizontal_hallway.check_orientation() == True


def test_invalid_hallway(invalid_hallway):
    with pytest.raises(Exception) as err:
        check_hallway(invalid_hallway)
        assert invalid_hallway in str(err.value)
    return False