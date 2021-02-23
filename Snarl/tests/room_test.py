import sys, os
import pytest
currentdir = os.path.dirname(os.path.realpath(__file__))
snarl_dir = os.path.dirname(currentdir)
game_dir = snarl_dir + '/Game'
sys.path.append(game_dir)
from room import Room
from coord import Coord

@pytest.fixture
def room1():
    tiles = [Coord(7, 6),Coord(7, 8),Coord(7, 9),Coord(7, 10), Coord(6, 6), Coord(6, 8), Coord(8, 9), Coord(8,6), Coord(8, 7), Coord(8,8), Coord(8, 9), Coord(8, 10), Coord(9, 6), Coord(9, 7), Coord(9,8), Coord(6, 10)]
    start = Coord(5, 5)
    dimensions = Coord(5, 5)
    doors = [Coord(8, 10), Coord(7, 10), Coord(6, 10)]
    items = [Coord(6, 6), Coord(7, 8)]
    room1 = Room(start, dimensions, tiles, doors, items)
    return room1


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




