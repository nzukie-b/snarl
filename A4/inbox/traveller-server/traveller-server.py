import json
import apgl

rpgMap = apgl.DictGraph()

# adds a town to the map
def create_town(name, connected_towns):
    rpgMap.setVertex(name, name)
    rpgMap.addEdges([(name, town) for town in connected_towns])

# places a character in specified town
# needs implementation of a Town class
def place_character(town, character):
    town.place_character(character)

# checks if a character can reach a town without passing other characters
def query_can_reach(character, town, characters, towns):
    not_occupied = []
    for t in towns:
        if t.characters == []:
            not_occupied.append(t)
    if town not in not_occupied:
        return False
    newMap = rpgMap.subgraph(not_occupied)
    distances = newMap.findAllDistances()
    if distances[character.town][town] != -1:
        return True
    else:
        return False