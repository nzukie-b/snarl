from constants import SIZE
from coord import Coord


class Adversary:
    def __init__(self, name, pos=None, health=100, non_walkable_tiles=["Wall"], movement_speed=1):
        self.pos = Coord(pos.row, pos.col) if pos else None
        self.name = name
        self.health = health
        self.non_walkable_tiles = non_walkable_tiles
        self.movement_speed = movement_speed
    
    def __str__(self):
        return '{{"pos": {}, "id": {}, "health": {}, "walkable_tiles": {}, "movement_speed": {}}}'.format(self.pos, self.name, self.health, self.non_walkable_tiles, self.movement_speed)

    def __repr__(self):
        return str(self)
