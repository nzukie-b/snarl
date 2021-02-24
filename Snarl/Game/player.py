from constants import SIZE
from coord import Coord


class Player:
    def __init__(self, pos, name, health, inventory=[]):
        self.pos = Coord(pos.x * SIZE, pos.y * SIZE)
        self.name = name
        self.inventory = inventory
        self.health = health
