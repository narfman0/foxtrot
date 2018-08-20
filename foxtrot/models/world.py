""" World contains multiple chunks, which are populated game sections """
import logging
import math
import operator
import random

from foxtrot.models.chunk import Planet, Ship, Station
from foxtrot.models.npc import NPC


logger = logging.getLogger(__name__)


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
        self.create_ship()

    def update(self):
        """ Update every tick """
        self.player.update(self)

    def create_player(self, chunk):
        x = chunk.x
        y = chunk.y
        offset = 64 + random.randint(0, 32)
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

    def create_ship(self):
        x = self.player.x
        y = self.player.y
        offset = random.randint(20, 24)
        if random.choice([True, False]):
            offset *= -1
        if random.choice([True, False]):
            x += offset
        else:
            y += offset

        # need to generate a ship with at least some # rooms:
        ship = None
        while ship is None:
            try:
                ship = Ship(random, x=x, y=y, width=16, height=16)
                if len(ship.tiles.rooms) < Ship.MIN_ROOMS:
                    ship = None
            except Exception as e:
                logger.warn("Failed to create ship with exception: %s, retrying", e)
        self.chunks.append(ship)

    def fly(self, origin, destination):
        x = destination.x - origin.x
        y = destination.y - origin.y
        direction = random.randint(0, 3)
        if direction == 0:
            # up
            x += destination.airlock_x - origin.airlock_x
            y += destination.height // 2 + origin.height // 2
        elif direction == 1:
            # right
            x += destination.width // 2 + origin.width // 2
            y += destination.airlock_y - origin.airlock_y
        elif direction == 2:
            # down
            x += destination.airlock_x - origin.airlock_x
            y -= destination.height // 2 + origin.height // 2
        else:
            # left
            x -= destination.width // 2 + origin.width // 2
            y += destination.airlock_y - origin.airlock_y
        origin.move(x, y)
        self.player.move(x, y)

    def get_destinations(self, x, y, sort=True):
        destinations = []
        for chunk in self.chunks:
            if not isinstance(chunk, Ship):
                distance = math.sqrt((x - chunk.x) ** 2 + (y - chunk.y) ** 2)
                destinations.append((distance, chunk))
        destinations = sorted(destinations, key=operator.itemgetter(0))
        return [destination[1] for destination in destinations]

    def npc_in_chunk(self, npc):
        """ return chunk if npc is in a chunk """
        for chunk in self.chunks:
            if chunk.aabb(npc.x, npc.y):
                return chunk
        return None
