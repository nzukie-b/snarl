#!/usr/bin/env python
import sys, os
import pytest
import pytest_check as check
currentdir = os.path.dirname(os.path.realpath(__file__))
game_dir = os.path.dirname(currentdir)
sys.path.append(game_dir)
from level import Coord, Room, Hallway, Level, Tile, check_room, check_hallway


#Room 1 example
tiles = [Coord(7, 6),Coord(7, 8),Coord(7, 9),Coord(7, 10), Coord(6, 6), Coord(6, 8), Coord(8, 9), Coord(8,6), Coord(8, 7), Coord(8,8), Coord(8, 9), Coord(8, 10), Coord(9, 6), Coord(9, 7), Coord(9,8), Coord(6, 10)]
start = Coord(5, 5)
dimensions = Coord(5, 5)
doors = [Coord(8,10), Coord(7, 10), Coord(6, 10)]
items = [Coord(6, 6), Coord(7, 8)]

@pytest.fixture
def room1():
    '''Initializes example Room'''
    room = Room(start, dimensions, tiles, doors, items)
    return room

@pytest.fixture
def invalid_tiles():
    '''Initializes example Room with invalid Tiles'''
    invalid_tiles = [Coord(11, 10), Coord(7, 6),Coord(7, 8),Coord(7, 9),Coord(7, 10), Coord(6, 6), Coord(6, 8), Coord(8, 9), Coord(8,6), Coord(8, 7), Coord(8,8), Coord(8, 9), Coord(8, 10), Coord(9, 6), Coord(9, 7), Coord(9,8), Coord(6, 10)]
    room = Room(start, dimensions, invalid_tiles, doors, items)
    return room

@pytest.fixture
def invalid_doors():
    '''Initializes example Room with invalid Doors'''
    invalid_doors = [Coord(8,10), Coord(7, 10), Coord(5, 5), Coord(6, 10)]
    room = Room(start, dimensions, tiles, invalid_doors, items)
    return room

@pytest.fixture
def hallway(room1):
    '''Initializes a Hallway with a vertical orientation'''
    hall_start = Coord(6, 10)
    hall = Hallway(hall_start, Coord(2, 3), [room1])
    return hall

@pytest.fixture 
def horizontal_hallway():
    '''Initializes a Hallway with a horizontal orientation'''
    hall_start = Coord(0, 0)
    hall = Hallway(hall_start, Coord(5, 5), [Room(start, dimensions, [Coord(5, 5)], [Coord(5, 3)])])
    return hall

@pytest.fixture
def invalid_hallway():
    hall_start = Coord(0, 0)
    hall = Hallway(hall_start, Coord(5, 5), [Room(start, dimensions, [Coord(5, 5)], [Coord(3, 3)])])
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


def test_coord(check):
    c1 = Coord(0, 0)
    c2 = Coord(0, 1)
    c3 = Coord(0, 0)
    check.is_false(c1 == c2)
    check.is_false(c2 == c3)
    assert c1 == c3


def test_valid_check_room(room1):
    assert check_room(room1) == True

def test_invalid_check_room(capsys, invalid_tiles, invalid_doors):
    valid_tiles = check_room(invalid_tiles)
    capture = capsys.readouterr()
    assert capture.out == 'Invalid Room: Walkable tile(s) outside of room dimensions\n'
    assert valid_tiles == False
    valid_doors = check_room(invalid_doors)
    capture = capsys.readouterr()
    assert capture.out == 'Invalid Room: Door(s) outside of walkable tiles\n'
    assert valid_doors == False

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


# def test_test(setup_hallway):
#     assert setup_hallway.check_orientation() == True