class Item:
    def __init__(self, type_, pos):
        self.type = type_
        self.pos = pos

    def __str__(self):
        return '{{"type": {}, "pos": {}}}'.format(self.type, self.pos)

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.type == other.type and self.pos == other.pos
        return False
        
    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.type, self.pos))