#!/usr/bin/env python
import json

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Coord):
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        return '{{"x": {}, "y":{}}}'.format(self.x, self.y)
