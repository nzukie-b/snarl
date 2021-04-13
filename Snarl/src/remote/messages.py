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

class RemoteActorUpdate(ActorUpdate):
    def __init__(self, type_, layout, pos, objects, actors, message=None):
        super().__init__(type_=type_, layout=layout, pos=pos, objects=objects, actors=actors)
        self.message = message
    
    def __str__(self):
        return '{{"type": {}, "layout": {}, "position": {}, "objects": {}, "actors": {}, "message": }}'.format(self.type, self.layout, self.pos, self.objects, self.actors, self.message)
        
        
        