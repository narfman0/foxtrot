""" A chunk is a meaningful part of the world. It includes bounding box of
coords, tiles, and possibly npcs. """
from foxtrot.models.chunk.generator import Generator


class Chunk:
    def __init__(self, random, x=None, y=None, planet=False, size=None, max_size=10000):
        self.random = random
        self.planet = planet
        self.size = (
            size if size is not None else 256 if planet else random.choice([64, 128])
        )
        self.x = (
            random.randint(self.size // 2, max_size - self.size // 2)
            if x is None
            else x
        )
        self.y = (
            random.randint(self.size // 2, max_size - self.size // 2)
            if y is None
            else y
        )
        self.npcs = []
        self.tiles = Generator(self.size, self.size)
        self.tiles.place_random_rooms(8, 16, 2, 1, 100)
        self.tiles.generate_corridors("l")
        self.tiles.connect_all_rooms(0)
        self.tiles.prune_deadends(50)
        self.tiles.join_unconnected_areas(self.tiles.find_unconnected_areas())

    def update(self):
        for npc in npcs:
            npc.update()

    def aabb(self, x, y):
        """ return True if x,y coords are inside this chunk """
        return abs(self.x - x) < self.size // 2 and abs(self.y - y) < self.size // 2
