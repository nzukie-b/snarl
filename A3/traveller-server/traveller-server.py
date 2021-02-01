#!/usr/bin/env python3

# Algorithm to find path from https://www.python.org/doc/essays/graphs/ with modification to exclude nodes with a character
def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    for node in graph[start]:
        if node not in path and node.char == None:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath
    return None


class Town_Network:
    def __init__(self):
        self.towns = None

    # Asssuming town is a dictionary with key being the name of the town,
    # and the value being a set of nodes that can be accessed from
    # i.e {'A': ['B', 'C', 'D']} with letters representing Town objects
    def add_town(self, town):
        self.towns = set(self.towns.append(town))

    def can_move(self, dest_town, char):
        origin = None
        for town in self.towns:
            if town.char == char:
                origin = town

        path = find_path(self.towns, origin, dest_town)
        return True if path else False

class Town:
    # assuming a town will be created with a name
    def __init__(self, name):
        self.name = name
        self.inTown = False
        self.char = None

    def place_char(self, char):
        self.inTown = True
        self.char = char

class Character:
    def __init__(self, name):
        self.name = name
