from foxtrot import log
from foxtrot.models import words

logger = log.create_logger(__name__)


class NPC:
    EVA_ACCELERATION = .002
    VELOCITY_IN_GRAVITY = .1

    def __init__(self, random=None, name=None, x=0, y=0, dx=0, dy=0):
        self.name = name if name else words.generate(random)
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
        self.move(self.dx, self.dy)
        old_chunk = self.chunk
        # npc can overlap many chunks (if traveling in ship, e.g.), so change
        # only if we aren't in originating chunk
        chunks = list(world.npc_in_chunk(self))
        if chunks and self.chunk not in chunks:
            self.chunk = chunks[0]
            if len(chunks) > 1:
                logger.warning("NPC %s in multiple chunks, choosing first", self)
        if not chunks:
            self.chunk = None

        if self.chunk and self.in_chunk != old_chunk:
            # make sure chunk is not on an impassable wall
            if not self.chunk.passable(self.x, self.y):
                self.move(-self.dx, -self.dy)
                self.dx = 0
                self.dy = 0
                self.chunk = old_chunk
            if self.chunk != old_chunk:
                logger.info(
                    "Adding npc %s to %s %s", self, type(old_chunk).__name__, self.chunk
                )
                self.chunk.npcs.add(self)
        if old_chunk is not None and self.chunk != old_chunk:
            old_chunk.npcs.remove(self)
            logger.info(
                "Removing npc %s from %s %s", self, type(old_chunk).__name__, old_chunk
            )

        self.in_chunk = bool(self.chunk)
        if self.in_chunk:
            self.dx = 0
            self.dy = 0
            self.room = self.chunk.get_room(self.x, self.y)
            self.in_room = bool(self.room)
        else:
            self.room = None
            self.in_room = False

    def move(self, x, y):
        self.x += x
        self.y += y

    @property
    def position(self):
        return self.x, self.y

    def __repr__(self):
        return self.name
