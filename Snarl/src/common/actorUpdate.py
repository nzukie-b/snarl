
class ActorUpdate:
    def __init__(self, type_=None, layout=None, position=None, objects=[], actors=[]):
        self.type = type_
        self.layout = layout
        self.position = position
        self.objects = objects
        self.actors = actors

    def __str__(self):
        return '{{"type": {}, "layout": {}, "position": {}, "objects": {}, "actors": {}}}'.format(self.type, self.layout, self.position, self.objects, self.actors)
    
    def __repr__(self):
        return str(self)