""" World contains multiple chunks, which are populated game sections """
import random

from foxtrot.models.chunk import Planet, Station
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
            self.chunks.append(Planet(random))
        for _ in range(station_count):
            self.chunks.append(Station(random))
        self.create_player(self.chunks[0])

    def update(self):
        """ Update every tick """
        self.player.update(self)

    def npc_in_chunk(self, npc):
        """ return chunk if npc is in a chunk """
        for chunk in self.chunks:
            if chunk.aabb(npc.x, npc.y):
                return chunk
        return None

    def create_player(self, chunk):
        x = chunk.x
        y = chunk.y
        offset = 8 + random.randint(0, 2)
        horizontal = random.choice([True, False])
        if horizontal:
            offset += chunk.width // 2
        else:
            offset += chunk.height // 2
        if random.choice([True, False]):
            offset *= -1
        if horizontal:
            x += offset
        else:
            y += offset
        self.player = NPC(x=x, y=y)

    def chunk_active(self, chunk):
        """ Check if chunk should be active or not """
        max_distance = 64
        return (
            abs(self.player.x - chunk.x) - chunk.width // 2 < max_distance
            and abs(self.player.y - chunk.y) - chunk.height // 2 < max_distance
        )
