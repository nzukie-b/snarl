import json
from constants import SIZE
from coord import Coord


class Adversary:
    def __init__(self, pos, name, health=100, non_walkable_tiles=["Wall"], movement_speed=1):
        self.pos = Coord(pos.row * SIZE, pos.col * SIZE)
        self.id = name
        self.health = health
        self.walkable_tiles = non_walkable_tiles
        self.movement_speed = movement_speed
    
    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return str(self)
