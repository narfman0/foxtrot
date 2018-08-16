""" World contains multiple chunks, which are populated game sections """
import random

from foxtrot.models.chunk import Chunk


class World:
    def __init__(self, seed=None, size=5):
        random.seed(seed)
        planet_count = random.randint(2 + size // 2, 3 + size // 2)
        station_count = random.randint(2 * size - 2, 2 * size + 2)
        self.chunks = []
        for _ in range(planet_count):
            self.chunks.append(Chunk(random, planet=True))
        for _ in range(station_count):
            self.chunks.append(Chunk(random))
        # TODO ensure chunks have a position in the world
