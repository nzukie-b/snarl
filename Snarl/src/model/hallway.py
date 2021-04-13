#!/usr/bin/env python
import json
from constants import ORIGIN
from coord import Coord

class Hallway:
    def __init__(self, doors, rooms, waypoints=None):
        # Doors are coordinates of door in connected room
        self.doors = doors
        self.rooms = rooms
        #Waypoints are alternate entrance point
        self.waypoints = waypoints if waypoints != None else []
        waypoint1 = doors[0]
        waypoint2 = doors[1] 
        self.origin = doors[0]
        try:
            waypoint1 = waypoints[0]
            self.origin = waypoint1
        except (TypeError, IndexError):
            pass
        try:
            waypoint2 = waypoints[1]
        except (TypeError, IndexError):
            pass

        self.dimensions = Coord(abs(waypoint2.row - waypoint1.row), abs(waypoint2.col - waypoint1.col)) 
    
    def __str__(self):
        doors_str = [str(door) for door in self.doors]
        dimensions_str = str(self.dimensions)
        rooms_str = [str(room) for room in self.rooms]
        waypoints_str = [str(waypoint) for waypoint in self.waypoints]
        return '{{"doors": {}, "dimensions": {}, "rooms": {}, "waypoints": {}}}'.format(doors_str, dimensions_str, rooms_str, waypoints_str)

    def __repr__(self):
        return str(self)

    def check_orientation(self):
        '''Check the orientation of the Hall. If True it is horizontal if False it is vertical otherwise an error is thrown'''
        is_horizontal = None
        door_1 = self.doors[0]
        door_2 = self.doors[1]

        if not self.waypoints:
            #Straight hallway no waypoints
            horizontal = door_1.row == door_2.row
            vertical = door_1.col == door_2.col
            if horizontal is not vertical:
                # horizontal xor vertical
                if horizontal:
                    is_horizontal = True
                else:
                    is_horizontal = False
                return is_horizontal
            else:
            #Not straight and no waypoint
                raise Exception(self)
        else:
            for ii in range(len(self.waypoints)):
                waypoint = self.waypoints[ii]
                if self.doors[ii].row == waypoint.row:
                    # Horizontal hallway
                    if is_horizontal == False:
                            # Waypoints should not be the same as doors.
                            raise Exception(self)
                    is_horizontal = True
                elif self.doors[ii].col == waypoint.col:
                    #Vertical Hallway
                    if is_horizontal == True:
                        raise Exception(self)
                is_horizontal = False
        return is_horizontal

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
    
    def in_hallway(self, coord):
        origin_row = self.origin.row
        origin_col = self.origin.col
        dest_row = self.origin.row + self.dimensions.row
        dest_col = self.origin.col + self.dimensions.col
        return coord.row in range(origin_row, dest_row + 1) and coord.col in range(origin_col, dest_col + 1)
                