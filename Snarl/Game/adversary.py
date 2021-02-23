from constants import SIZE
from coord import Coord

class Adversary:
    def __init__(self, pos, id, health):
        self.pos = Coord(pos.x * SIZE, pos.y * SIZE)
        self.id = id
        self.health = health
