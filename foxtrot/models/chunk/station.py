from foxtrot.models.chunk.chunk import Chunk


class Station(Chunk):
    SIZES = [32, 64]

    def __init__(
        self, random, name=None, x=None, y=None, width=None, height=None, max_size=10000
    ):
        size = random.choice(self.SIZES)
        width = width if width else size
        height = height if height else size
        Chunk.__init__(
            self,
            random,
            name=name,
            x=x,
            y=y,
            width=width,
            height=height,
            max_size=max_size,
        )
        self.initialize_traders(random)
