#!/usr/bin/env python

# Assuming that dimension given will not be offset from the origin and will just be sized dimensions in x and y.
#   ie. origin = (10, 10) dimensions = (5, 7) The tile boundaries of the room are (10 - 15, 10 - 17)
class Room:
    def __init__(self, origin, dimensions, tiles, doors, items=None):
        self.origin = origin
        self.dimensions = dimensions
        self.tiles = tiles
        self.doors = doors
        self.items = items if items != None else []

    def check_doors(self):
        ''' Validate doors are on a walkable tiles. Does not guarantee that tiles are inside room boundaries'''
        for door in self.doors:
            if door not in self.tiles:
                return False
        return True
    
    def check_tiles(self):
        '''Validate walkable tiles are inside the room boundaries'''
        for tile in self.tiles:
            if tile.x not in range(self.origin.x , self.origin.x + self.dimensions.x) and tile.y not in range(self.origin.y, self.origin.y + self.dimensions.y):
                return False
        return True

    # Validate items are on a walkable tile?
    def check_items(self):
        '''Validate items are on a walkable tile'''
        for item in self.items:
            if item.x not in self.tiles:
                # TODO: Are items on non walkable tiles valid?
                return False
        return True

    def get_reachable_tiles(self, coord):
        '''Returns a list of reachable tiles in this room within a 1 space move'''
        tiles = []
        for tile in self.tiles:
            if (tile.x == coord.x) and (tile.y ==  coord.y + 1 or tile.y == coord.y - 1):
                tiles.append(tile)
            elif (tile.y == coord.y) and (tile.x == coord.x + 1 or tile.x == coord.x - 1):
                tiles.append(tile)
        return tiles

    def is_reachable_tile(self, coord):
        return coord in self.tiles

