#!/usr/bin/env python
import json

# Assuming that dimension given will not be offset from the origin and will just be sized dimensions in x and y.
#   ie. origin = (10, 10) dimensions = (5, 7) The tile boundaries of the room are (10 - 15, 10 - 17)
class Room:
    def __init__(self, origin, dimensions, tiles, doors, items=None):
        self.origin = origin
        self.dimensions = dimensions
        self.tiles = tiles
        self.doors = doors
        self.items = items if items != None else []
    
    def __str__(self):
        origin_str = str(self.origin)
        dimensions_str = str(self.dimensions)
        tiles_str = [str(tile) for tile in self.tiles]
        doors_str = [str(door) for door in self.doors]
        items_str = [str(item) for item in self.items]
        return '{{"origin": {}, "dimensions": {}, "tiles": {}, "doors": {}, "items": {}}}'.format(
            origin_str, dimensions_str, tiles_str, doors_str, items_str)

    def __repr__(self):
        return str(self)

    def check_doors(self):
        ''' Validate doors are on a walkable tiles. Does not guarantee that tiles are inside room boundaries'''
        for door in self.doors:
            if door not in self.tiles:
                return False
        return True
    
    def check_tiles(self):
        '''Validate walkable tiles are inside the room boundaries'''
        for tile in self.tiles:
            if tile.row not in range(self.origin.row , self.origin.row + self.dimensions.row + 1) and tile.col not in range(self.origin.col, self.origin.col + self.dimensions.col + 1):
                return False
        return True

    # Validate items are on a walkable tile?
    def check_items(self):
        '''Validate items are on a walkable tile'''
        for item in self.items:
            if item not in self.tiles:
                # TODO: Are items on non walkable tiles valid?
                return False
        return True

    def get_reachable_tiles(self, coord):
        '''Returns a list of reachable tiles in this room within a 1 space move'''
        tiles = []
        for tile in self.tiles:
            #TODO: Separate this into some coord comparison function?
            if (tile.row == coord.row) and (tile.col ==  coord.col + 1 or tile.col == coord.col - 1):
                tiles.append(tile)
            elif (tile.col == coord.col) and (tile.row == coord.row + 1 or tile.row == coord.row - 1):
                tiles.append(tile)
        return tiles

    def is_reachable_tile(self, coord):
        return coord in self.tiles

