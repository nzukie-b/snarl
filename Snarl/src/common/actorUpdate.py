
class ActorUpdate:
    def __init__(self, type_=None, layout=None, pos=None, objects=None, actors=None):
        self.type = type_
        self.layout = layout
        self.pos = pos
        self.objects = objects if objects else []
        self.actors = actors if actors else []
        self.layout_coords = None

    def __str__(self):
        return '{{"type": {}, "layout": {}, "position": {}, "objects": {}, "actors": {}}}'.format(self.type, self.layout, self.pos, self.objects, self.actors)
    
    def __repr__(self):
        return str(self)