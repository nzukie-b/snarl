import sys, os, json

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from constants import END_GAME, END_LEVEL, P_SCORE, START_LVL, WELCOME
class Welcome:
    def __init__(self, server_info):
        self.type = WELCOME
        self.info = server_info
    
    def __str__(self):
        return json.dumps({"type": self.type, "info": self.info})
class StartLevel:
    def __init__(self, level, players):
        self.type = START_LVL
        self.level = level
        self.players = players

    def __str__(self):
        return json.dumps({"type": self.type, "level": self.level, "players": self.players})

class ActorPosition:
    def __init__(self, type_, name, pos):
        self.type = type_
        self.name = name
        self.pos = pos

    def __str__(self):
        return json.dumps({"type": self.type, "name": self.name, "position": self.pos})

    def __repr__(self) -> str:
        return str(self)
class ObjectPos:
    def __init__(self, type_, pos):
        self.type = type_
        self.pos = pos
    
    def __str__(self):
        return json.dumps({"type": self.type, "position": self.pos})

    def __repr__(self) -> str:
        return str(self)
        
class RemoteActorUpdate:
    def __init__(self, type=None, layout=None, position=None, objects=None, actors=None, message=None):
        #  type instead of type_ to make it easier to serialize json into this obj
        self.type = type
        self.layout = layout
        self.position = position
        self.objects = objects if objects else []
        self.actors = actors if actors else []
        self.layout_coords = None
        self.message = message
    
    def __str__(self):
       return json.dumps({"type": self.type, "layout": self.layout, "position": [self.position.row, self.position.col], "objects": self.objects, "message": self.message})

    def __repr__(self):
        return str(self)

class ActorMove:
    def __init__(self, to):
        self.type = 'move'
        self.to = to
    def __str__(self) -> str:
        return json.dumps({"type": self.type, "to": self.to})

    def __repr(self):
        return str(self)
        
class EndLevel:
    def __init__(self, key, exits, ejects):
        self.type = END_LEVEL
        self.key = key
        self.exits = exits
        self.ejects = ejects

    def __str__(self):
        return json.dumps({"type": self.type, "key": self.key, "exits": self.exits, "ejects": self.ejects})

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
        return json.dumps({"type": self.type, "name": self.name, "keys": self.keys, "exits": self.exits, "ejects": self.ejects})

    def __repr__(self) -> str:
        return str(self)

class EndGame:
    def __init__(self, scores):
        self.type = END_GAME
        self.scores = scores

    def __str__(self):
        # scores_str = [str(score) for score in self.scores]
        #TODO: Double check formatting on scores_str 
        scores_str = [str(score) for score in self.scores]
        return json.dumps({"type": self.type, "scores": scores_str})

    def __repr__(self) -> str:
        return str(self)
