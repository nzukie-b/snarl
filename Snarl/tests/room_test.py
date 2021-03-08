import sys, os
import pytest
currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/src'
sys.path.append(game_dir)
from model.room import Room
from coord import Coord
from utilities import check_room


#Room 1 example
tiles = [Coord(7, 6),Coord(7, 8),Coord(7, 9),Coord(7, 10), Coord(6, 6), Coord(6, 8), Coord(8, 9), Coord(8,6), Coord(8, 7), Coord(8,8), Coord(8, 9), Coord(8, 10), Coord(9, 6), Coord(9, 7), Coord(9,8), Coord(6, 10)]
start = Coord(5, 0)
dimensions = Coord(5, 5)
doors = [Coord(7, 10)]
items = [Coord(6, 6), Coord(7, 8)]


@pytest.fixture
def room1():
    tiles = [Coord(7, 6),Coord(7, 8),Coord(7, 9),Coord(7, 10), Coord(6, 6), Coord(6, 8), Coord(8, 9), Coord(8,6), Coord(8, 7), Coord(8,8), Coord(8, 9), Coord(8, 10), Coord(9, 6), Coord(9, 7), Coord(9,8), Coord(6, 10)]
    start = Coord(5, 5)
    dimensions = Coord(5, 5)
    doors = [Coord(8, 10), Coord(7, 10), Coord(6, 10)]
    items = [Coord(6, 6), Coord(7, 8)]
    room1 = Room(start, dimensions, tiles, doors, items)
    return room1

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

def test_reachable_tiles_single(room1):
    coord = Coord(6, 6)
    tiles = room1.get_reachable_tiles(coord)
    assert len(tiles) == 1
    assert Coord(7, 6) in tiles

def test_reachable_tiles_multiple(room1):
    coord = Coord(8, 7)
    tiles = room1.get_reachable_tiles(coord)
    assert len(tiles) == 3
    assert Coord(8, 6) in tiles
    assert Coord (8, 8) in tiles
    assert Coord(9, 7) in tiles




