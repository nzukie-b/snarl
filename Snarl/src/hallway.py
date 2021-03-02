#!/usr/bin/env python
import json
from coord import Coord

class Hallway:
    def __init__(self, origin, dimensions, rooms, waypoints=None):
        self.origin = origin
        self.dimensions = dimensions
        self.rooms = rooms
        self.waypoints = waypoints if waypoints != None else []
    
    def __str__(self):
        origin_str = str(self.origin)
        dimensions_str = str(self.dimensions)
        rooms_str = [str(room) for room in self.rooms]
        waypoints_str = [str(waypoint) for waypoint in self.waypoints]
        return '{{"origin": {}, "dimensions": {}, "rooms": {}, "waypoints": {}}}'.format(origin_str, dimensions_str, rooms_str, waypoints_str)


    def check_orientation(self):
        '''Check the orientation of the Hall. If True it is horizontal if False it is vertical otherwise an error is thrown'''
        is_horizontal = None
        for room in self.rooms:
            for door in room.doors:
                if (door.y == self.origin.y - 1 or door.y == self.origin.y + self.dimensions.y + 1) and (self.origin.x <= door.x <= self.origin.x + self.dimensions.x):
                    if is_horizontal is True:
                        raise Exception(self)
                    is_horizontal = False
                elif (door.x == self.origin.x  - 1 or door.x == self.origin.x + self.dimensions.x + 1) and (self.origin.y <= door.y <= self.origin.y + self.dimensions.y):
                    if is_horizontal is False:
                        raise Exception(self)
                    is_horizontal = True                        
        return is_horizontal

    def get_reachable_tiles(self, coord):
        try:
            tiles = []
            is_horizontal = self.check_orientation()
            # If halls should be 1 tile wide any traversable coord in a horizontal hall must have the same y value as a door. The range of traversable tiles spans the x boundary while y does not change
            if is_horizontal == True:
                y_values = set()
                for room in self.rooms:
                    for door in room.doors:
                        y_values.add(door.y)
                for ii in range(self.origin.x, self.origin.x + self.dimensions.x + 1):
                    if coord.y in y_values:
                        new_coord = Coord(ii, coord.y)
                        tiles.append(new_coord)
            elif is_horizontal == False:
                x_values = set()
                for room in self.rooms:
                    for door in room.doors:
                        x_values.add(door.x)
                for jj in range(self.origin.y, self.origin.y + self.dimensions.y + 1):
                    if coord.x in x_values:
                        new_coord = Coord(coord.x, jj)
                        tiles.append(new_coord)
            return tiles
        except Exception as err:
            print(err)
            return None
                