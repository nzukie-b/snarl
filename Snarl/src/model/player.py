from constants import SIZE
from coord import Coord


class PlayerActor:
    def __init__(self, name, pos=None, health=100, inventory=[], non_walkable_tiles=["Wall"], move_speed=2):
        self.name = name
        self.pos = Coord(pos.row, pos.col) if pos else None
        self.inventory = inventory
        self.health = health
        self.non_walkable_tiles = non_walkable_tiles
        self.move_speed = move_speed

    def __str__(self):
        return '{{"pos": {}, "name": {}, "health": {}, "walkable_tiles": {}, "move_speed": {}, "inventory": {}}}'.format(self.pos, self.name, self.health, self.non_walkable_tiles, self.move_speed, self.inventory)

    def __repr__(self):
        return str(self)
