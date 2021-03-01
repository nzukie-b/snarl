from constants import SIZE
from coord import Coord


class Player:
    def __init__(self, pos, name, health, inventory=[], non_walkable_tiles=["Wall"], movement_speed=2):
        self.pos = Coord(pos.x * SIZE, pos.y * SIZE)
        self.name = name
        self.inventory = inventory
        self.health = health
        self.non_walkable_tiles = non_walkable_tiles
        self.movement_speed = movement_speed