#!/usr/bin/env python
import json

class Coord:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def __eq__(self, other):
        if isinstance(other, Coord):
            return self.row == other.row and self.col == other.col
        return False
    def __str__(self):
        return '{{"row": {}, "col":{}}}'.format(self.row, self.col)
