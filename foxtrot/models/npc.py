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
        self.room = None
        self.in_room = False

    def update(self, world):
        self.x += self.dx
        self.y += self.dy
        self.chunk = world.npc_in_chunk(self)

        if self.chunk is not None and not self.in_chunk:
            # we just entered a chunk, make sure its not on an impassable wall
            if not self.chunk.passable(self.x, self.y):
                self.x -= self.dx
                self.y -= self.dy

        self.in_chunk = bool(self.chunk)
        if self.in_chunk:
            self.dx = 0
            self.dy = 0
            self.room = self.chunk.get_room(self.x, self.y)
            self.in_room = bool(self.room)
