class NPC:
    def __init__(self, name=None, x=0, y=0, dx=0, dy=0):
        self.name = name
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def update(self):
        self.x += self.dx
        self.y += self.dy
