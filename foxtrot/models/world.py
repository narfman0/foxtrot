""" World contains multiple chunks, which are populated game sections """
import random

from foxtrot.models.chunk import Chunk
from foxtrot.models.npc import NPC


class World:
    def __init__(self, seed=None, size=0):
        """ Create world with given seed, will generate using system timestamp
        if none given. Size expected in the range (0-10)
        """
        random.seed(seed)
        planet_count = random.randint(2 + size // 2, 3 + size // 2)
        station_count = random.randint(2 * size - 2, 2 * size + 2)
        self.chunks = []
        for _ in range(planet_count):
            self.create_chunk(True)
        for _ in range(station_count):
            self.create_chunk(False)
        self.create_player(self.chunks[0])

    def create_chunk(self, planet, max_size=10000):
        """ Create a chunk with a generated position
        TODO ensure we dont collide with another chunk via bounding box
        """
        chunk = Chunk(random)
        x = random.randint(chunk.size // 2, max_size - chunk.size // 2)
        y = random.randint(chunk.size // 2, max_size - chunk.size // 2)
        self.chunks.append((x, y, chunk))

    def create_player(self, chunk_tuple):
        chunk_x, chunk_y, chunk = chunk_tuple
        self.player = NPC(x=chunk_x, y=chunk_y)
