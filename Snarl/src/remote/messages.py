import sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)
from constants import START_LVL, WELCOME
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

class ActorPosition():
    def __init__(self, type_, name, pos):
        self.type = type_
        self.name = name
        self.pos = pos

    def __str__(self):
        return '{{"type" {}, "name": {}, "position": {}}}'.format(self.type, self.name, self.pos)

    def __repr__(self) -> str:
        return str(self)
class ObjectPos():
    def __init__(self, type_, pos):
        self.type = type_
        self.pos = pos
    
    def __str__(self):
        return '{{"type": {}, "position": {}}}'.format(self.type, self.pos)

    def __repr__(self) -> str:
        return str(self)
        
class RemoteActorUpdate():
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
        