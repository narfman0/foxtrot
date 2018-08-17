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

    def create_chunk(self, planet):
        """ Create a chunk with a generated position
        TODO ensure we dont collide with another chunk via bounding box
        """
        chunk = Chunk(random)
        self.chunks.append(chunk)

    def create_player(self, chunk):
        x = chunk.x
        y = chunk.y
        offset = chunk.size // 2 + 5 + random.randint(0, 2)
        if random.choice([True, False]):
            offset *= -1
        if random.choice([True, False]):
            x += offset
        else:
            y += offset
        self.player = NPC(x=x, y=y)

    def chunk_active(self, chunk):
        """ Check if chunk should be active or not """
        max_distance = 64
        return (
            abs(self.player.x - chunk.x) - chunk.size // 2 < max_distance
            and abs(self.player.y - chunk.y) - chunk.size // 2 < max_distance
        )
