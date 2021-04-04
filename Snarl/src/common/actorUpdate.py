
class ActorUpdate:
    def __init__(self, type_=None, layout=None, pos=None, objects=[], actors=[]):
        self.type = type_
        self.layout = layout
        self.pos = pos
        self.objects = objects
        self.actors = actors
        self.layout_coords = None

    def __str__(self):
        return '{{"type": {}, "layout": {}, "position": {}, "objects": {}, "actors": {}}}'.format(self.type, self.layout, self.pos, self.objects, self.actors)
    
    def __repr__(self):
        return str(self)