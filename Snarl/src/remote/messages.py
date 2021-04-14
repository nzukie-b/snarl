import sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from constants import END_GAME, END_LEVEL, P_SCORE, START_LVL, WELCOME
from common.actorUpdate import ActorUpdate

class Welcome:
    def __init__(self, server_info):
        self.type = WELCOME
        self.info = server_info
    
    def __str__(self):
        return '{{"type": {}, "info": {}}}'.format(self.type, self.info)

class StartLevel:
    def __init__(self, level, players):
        self.type = START_LVL
        self.level = level
        self.players = players

    def __str__(self):
        return '{{"type": {}, "level": {}, "players": {}'.format(self.type, self.level, self.players)

class ActorPosition:
    def __init__(self, type_, name, pos):
        self.type = type_
        self.name = name
        self.pos = pos

    def __str__(self):
        return '{{"type" {}, "name": {}, "position": {}}}'.format(self.type, self.name, self.pos)

    def __repr__(self) -> str:
        return str(self)
class ObjectPos:
    def __init__(self, type_, pos):
        self.type = type_
        self.pos = pos
    
    def __str__(self):
        return '{{"type": {}, "position": {}}}'.format(self.type, self.pos)

    def __repr__(self) -> str:
        return str(self)
        
class RemoteActorUpdate:
    def __init__(self, type_=None, layout=None, pos=None, objects=[], actors=[], message=None):
        self.type = type_
        self.layout = layout
        self.pos = pos
        self.objects = objects
        self.actors = actors
        self.layout_coords = None
        self.message = message
    
    def __str__(self):
        return '{{"type": {}, "layout": {}, "position": {}, "objects": {}, "actors": {}, "message": }}'.format(self.type, self.layout, self.pos, self.objects, self.actors, self.message)

    def __repr__(self):
        return str(self)
        
class EndLevel:
    def __init__(self, key, exits, ejects):
        self.type = END_LEVEL
        self.key = key
        self.exits = exits
        self.ejects = ejects

    def __str__(self):
        return '{{"type": {}, "key": {}, "exits": {}, "ejects": {}}}'.format(self.type, self.key, self.exits, self.ejects)

    def __repr__(self) -> str:
        return str(self)


class PlayerScore:
    def __init__(self, name, keys=0, exits=0, ejects=0):
        self.type = P_SCORE
        self.name = name
        self.keys = keys
        self.exits = exits
        self.ejects = ejects   

    def __str__(self) -> str:
        return '{{"type": {}, "name": {}, "keys": {} "exits": {}, "ejects": {}}}'.format(self.type, self.name, self.keys, self.exits, self.ejects)

    def __repr__(self) -> str:
        return str(self)

class EndGame:
    def __init__(self, scores):
        self.type = END_GAME
        self.score = scores

    def __str__(self):
        # scores_str = [str(score) for score in self.scores]
        #TODO: Double check formatting on scores_str 
        return '{{"type": {}, "scores": {}}}'.format(self.type, self.scores)

    def __repr__(self) -> str:
        return str(self)