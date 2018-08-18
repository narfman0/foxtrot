from foxtrot.models.chunk.chunk import Chunk


class Station(Chunk):
    SIZES = [32, 64]

    def __init__(self, random, x=None, y=None, width=None, height=None, max_size=10000):
        size = random.choice(self.SIZES)
        Chunk.__init__(
            self, random, x=x, y=y, width=size, height=size, max_size=max_size
        )
