""" A chunk is a meaningful part of the world. It includes bounding box of
coords, tiles, and possibly npcs. """
from foxtrot.models.chunk.generator import Generator


class Chunk:
    def __init__(self, random, planet=False, size=None):
        self.random = random
        self.planet = planet
        if size:
            self.size = size
        else:
            self.size = 256 if planet else random.choice([64, 128])
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
