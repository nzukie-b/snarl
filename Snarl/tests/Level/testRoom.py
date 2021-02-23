#!/usr/bin/env python

import json
import os


class Bounds:
    def __init__(self, rows, cols):
        self.rows = rows
        self.columns = cols

class Room:
    def __init__(self, origin, bounds, layout):
        self.type =  'room'
        self.origin = origin
        self.bounds = bounds
        self.layout = layout
