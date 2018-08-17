class NPC:
    EVA_ACCELERATION = .002
    VELOCITY_IN_GRAVITY = .1

    def __init__(self, name=None, x=0, y=0, dx=0, dy=0):
        self.name = name
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        # some physics helpers, speeds things up
        self.chunk = None
        self.in_chunk = False

    def update(self, world):
        self.chunk = world.npc_in_chunk(self)
        self.in_chunk = self.chunk is not None
        self.x += self.dx
        self.y += self.dy
        if self.in_chunk:
            self.dx = 0
            self.dy = 0
