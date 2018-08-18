from foxtrot.models.chunk.chunk import Chunk


class Planet(Chunk):
    SIZE = 128

    def __init__(self, random, x=None, y=None, width=None, height=None, max_size=10000):
        width = width if width else self.SIZE
        height = height if height else self.SIZE
        Chunk.__init__(
            self, random, x=x, y=y, width=width, height=height, max_size=max_size
        )
