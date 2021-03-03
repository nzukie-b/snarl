#!/usr/bin/env python
import json
from coord import Coord

class Hallway:
    def __init__(self, doors, rooms, waypoints=None):
        self.doors = doors
        self.rooms = rooms
        self.doors = doors
        self.waypoints = waypoints if waypoints != None else []
        row_dimensions = (min(doors[0].row, doors[1].row), max(doors[0].row, doors[1].row))
        col_dimensions = (min(doors[0].col, doors[1].col), max(doors[0].col, doors[1].col))
        self.origin = Coord(row_dimensions[0], col_dimensions[0])
        self.dimensions = Coord(row_dimensions[1] - row_dimensions[0], col_dimensions[1] - col_dimensions[0]) 
    
    def __str__(self):
        doors_str = [str(door) for door in self.doors]
        dimensions_str = str(self.dimensions)
        rooms_str = [str(room) for room in self.rooms]
        waypoints_str = [str(waypoint) for waypoint in self.waypoints]
        return '{{"doors": {}, "dimensions": {}, "rooms": {}, "waypoints": {}}}'.format(doors_str, dimensions_str, rooms_str, waypoints_str)


    # def check_orientation(self):
    #     #TODO: ADD SUPPORT FOR WAYPOINTS
    #     '''Check the orientation of the Hall. If True it is horizontal if False it is vertical otherwise an error is thrown'''
    #     is_horizontal = None
    #     #From Milestone 2 spec hallways have 2 rooms to connect. So only two doors
    #     if waypo
    #     for door in self.doors:
    #         if (door.x)
    #     for room in self.rooms:
    #         for door in room.doors:
    #             if (door.y == self.origin.y - 1 or door.y == self.origin.y + self.dimensions.y + 1) and (self.origin.x <= door.x <= self.origin.x + self.dimensions.x):
    #                 if is_horizontal is True:
    #                     raise Exception(self)
    #                 is_horizontal = False
    #             elif (door.x == self.origin.x  - 1 or door.x == self.origin.x + self.dimensions.x + 1) and (self.origin.y <= door.y <= self.origin.y + self.dimensions.y):
    #                 if is_horizontal is False:
    #                     raise Exception(self)
    #                 is_horizontal = True                        
    #     return is_horizontal

    def get_reachable_tiles(self, coord):
        try:
            tiles = []
            is_horizontal = self.check_orientation()
            # If halls should be 1 tile wide any traversable coord in a horizontal hall must have the same y value as a door. The range of traversable tiles spans the x boundary while y does not change
            if is_horizontal == True:
                col_values = set()
                for room in self.rooms:
                    for door in room.doors:
                        col_values.add(door.col)
                for ii in range(self.origin.row, self.origin.row + self.dimensions.row + 1):
                    if coord.col in col_values:
                        new_coord = Coord(ii, coord.col)
                        tiles.append(new_coord)
            elif is_horizontal == False:
                row_values = set()
                for room in self.rooms:
                    for door in room.doors:
                        row_values.add(door.row)
                for jj in range(self.origin.col, self.origin.col + self.dimensions.col + 1):
                    if coord.row in row_values:
                        new_coord = Coord(coord.row, jj)
                        tiles.append(new_coord)
            return tiles
        except Exception as err:
            print(err)
            return None
                