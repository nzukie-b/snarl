#!/usr/bin/env python

class Hallway:
    def __init__(self, origin, dimensions, rooms, waypoints=None):
        self.origin = origin
        self.dimensions = dimensions
        self.rooms = rooms
        self.waypoints = waypoints if waypoints != None else []


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