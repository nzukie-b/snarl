
import json
from abc import ABC
from coord import Coord

class Actor(ABC):
    def __init__(self, name, pos=None, health=100, non_walkable_tiles=["Wall"], move_speed=2, atk_power=0):
        self.name = name
        self.pos = Coord(pos.row, pos.col) if pos else None
        self.health = health
        self.non_walkable_tiles = non_walkable_tiles
        self.move_speed = move_speed
        self.atk_power = atk_power

    def __str__(self):
        inventory_str = str(self.inventory)
        return json.dumps({"pos": str(self.pos), "name": self.name, "health": self.health, "walkable_tiles": self.non_walkable_tiles, "move_speed": self.move_speed, "inventory": inventory_str})

    def __repr__(self):
        return str(self)
