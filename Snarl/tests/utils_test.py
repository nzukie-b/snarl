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
from utilities import check_dimensions, to_coord, to_point



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
def hallway(room3, room2):
    '''Initializes a Hallway with a vertical orientation'''
    hall = Hallway([Coord(7, 5), Coord(7, 15)], [room3, room2])
    return hall


@pytest.fixture
def level2(room3, room2, hallway):
    level = Level([room3, room2], [hallway], [Coord(7, 1)], [Coord(9, 17)])
    return level

def test_check_dimensions_rooms(level2, room3, room2, hallway):
    cd1 = Coord(5, 0)
    cd1_rows = (cd1.row, cd1.row)
    cd1_cols = (cd1.col, cd1.col)
    level_dimensions = level2.get_level_room_dimensions().union(level2.get_level_hallway_dimensions())
    res = check_dimensions(cd1_rows, cd1_cols, level_dimensions)
    assert res == room3.origin
    cd2_rows = (10, 10)
    cd2_cols = (20, 20)
    res = check_dimensions(cd2_rows, cd2_cols, level_dimensions)
    assert res == room2.origin

def test_check_dimensions_hallways(level2, room3, room2, hallway):
    level_dimensions = level2.get_level_room_dimensions().union(level2.get_level_hallway_dimensions())
    cd3_rows = (7, 7)
    cd3_cols = (6, 6)
    res = check_dimensions(cd3_rows, cd3_cols, level_dimensions)
    assert res == hallway.origin
    
def test_check_dimensions_no_match(level2, room3, room2, hallway):
    level_dimensions = level2.get_level_room_dimensions().union(level2.get_level_hallway_dimensions())
    cd4_rows = (0, 0)
    cd4_cols = (0, 0)
    res = check_dimensions(cd4_rows, cd4_cols, level_dimensions)
    assert res == None

def test_to_coord():
    c1 = Coord(0, 0)
    c2 = to_coord([0, 0])
    assert c1 == c2

def test_to_point():
    p1 = [0, 0]
    p2 = to_point(Coord(0, 0))
    assert p1[0] == p2[0]
    assert p1[1] == p2[1]

