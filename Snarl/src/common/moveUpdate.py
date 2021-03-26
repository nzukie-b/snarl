class MoveUpdate:
    def __init__(self, name=None, move=None, result=None):
        self.name = name
        self.move = move
        self.result = result
    def __str__(self):
        return '[{}, {}, {}]'

    def __repr__(self):
        return str(self)