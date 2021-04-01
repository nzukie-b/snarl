from constants import SIZE
from coord import Coord
from constants import ZOMBIE


class AdversaryActor:
    def __init__(self, name, type_=None, pos=None, health=100, non_walkable_tiles=["Wall"], movement_speed=1):
        self.pos = Coord(pos.row, pos.col) if pos else None
        self.name = name
        self.type = type_ if type_ else ZOMBIE
        self.health = health
        self.non_walkable_tiles = non_walkable_tiles
        self.movement_speed = movement_speed
    
    def __str__(self):
        return '{{"pos": {}, "name": {}, "health": {}, "walkable_tiles": {}, "movement_speed": {}}}'.format(self.pos, self.name, self.health, self.non_walkable_tiles, self.movement_speed)

    def __repr__(self):
        return str(self)
