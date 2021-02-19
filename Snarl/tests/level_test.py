#!/usr/bin/env python
import sys, os
import pytest
currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/Game'
sys.path.append(game_dir)
from coord import Coord
from room import Room
from hallway import Hallway
from level import Level, Tile
from utilities import check_room, check_hallway, check_level


#Room 1 example
tiles = [Coord(7, 6),Coord(7, 8),Coord(7, 9),Coord(7, 10), Coord(6, 6), Coord(6, 8), Coord(8, 9), Coord(8,6), Coord(8, 7), Coord(8,8), Coord(8, 9), Coord(8, 10), Coord(9, 6), Coord(9, 7), Coord(9,8), Coord(6, 10)]
start = Coord(5, 5)
dimensions = Coord(5, 5)
doors = [Coord(8, 10), Coord(7, 10), Coord(6, 10)]
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
    hall_start = Coord(6, 11)
    hall = Hallway(hall_start, Coord(2, 3), [room1])
    return hall

@pytest.fixture 
def horizontal_hallway():
    '''Initializes a Hallway with a horizontal orientation'''
    hall_start = Coord(0, 0)
    hall = Hallway(hall_start, Coord(4, 5), [Room(start, dimensions, [Coord(5, 3)], [Coord(5, 3)])])
    return hall

@pytest.fixture
def invalid_hallway():
    hall_start = Coord(0, 0)
    hall = Hallway(hall_start, Coord(5, 5), [Room(start, dimensions, [Coord(5, 5)], [Coord(3, 3)])])
    return hall


@pytest.fixture
def room2():
    #Room 2 example
    tiles1 = [Coord(7, 15), Coord(7, 17), Coord(7, 18), Coord(6, 17), Coord(8, 17), Coord(8, 15), 
                Coord(6, 15), Coord(7, 15), Coord(7, 15), Coord(9, 17), Coord(9, 16), Coord(9, 15), Coord (9, 15), Coord(6, 16)]
    start1 = Coord(5, 15)
    dimensions1 = Coord(5, 5)
    doors1 = [Coord(8, 15), Coord(7, 15), Coord(6, 15)]
    items1 = [Coord(8, 17), Coord(7, 17)]
    room2 = Room(start1, dimensions1, tiles1, doors1, items1)
    return room2

@pytest.fixture
def level1(room1, room2, hallway):
    level = Level([room1, room2], [hallway])
    return level



def test_coord():
    c1 = Coord(0, 0)
    c2 = Coord(0, 1)
    c3 = Coord(0, 0)
    assert c1 != c2
    assert c2 != c3
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
    hall2 = Hallway(Coord(6, 11), Coord(2, 3), [room1])
    level = Level([room1], [hallway, hall2])
    valid_level = check_level(level)
    capture = capsys.readouterr()
    assert capture.out == 'Invalid Level: Duplicate hallways\n'
    assert valid_level == False

def test_invalid_level_shared_coords(capsys, room1, level1):
    hall = Hallway(Coord(5, 5), Coord(5,5), [room1])
    level1.hallways.append(hall)
    valid_level = check_level(level1)
    capture = capsys.readouterr()
    assert capture.out == 'Invalid Level: Hallway or Room sharing coordinates\n'
    assert valid_level == False

def test_invalid_level_dimensions(capsys, level1):
    invalid_dimensions = Room(Coord(6, 6), Coord(6, 6), tiles, doors)
    level1.rooms.append(invalid_dimensions)
    valid_level = check_level(level1)
    capture = capsys.readouterr()
    assert capture.out == 'Invalid Level: Overlapping Room(s) or Hallway(s)\n'
    assert valid_level == False
    

# def test_test(setup_hallway):
#     assert setup_hallway.check_orientation() == True