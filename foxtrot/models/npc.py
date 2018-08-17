class NPC:
    VELOCITY_IN_GRAVITY = .1
    EVA_ACCELERATION = .002

    def __init__(self, name=None, x=0, y=0, dx=0, dy=0):
        self.name = name
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def update(self, world):
        self.x += self.dx
        self.y += self.dy
        if world.npc_in_chunk(self):
            self.dx = 0
            self.dy = 0
