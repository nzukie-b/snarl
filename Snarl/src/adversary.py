from constants import SIZE
from coord import Coord


class Adversary:
    def __init__(self, pos, id, health, non_walkable_tiles=["Wall"], movement_speed=1):
        self.pos = Coord(pos.x * SIZE, pos.y * SIZE)
        self.id = id
        self.health = health
        self.walkable_tiles = non_walkable_tiles
        self.movement_speed = movement_speed
