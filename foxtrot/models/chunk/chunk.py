""" A chunk is a meaningful part of the world. It includes bounding box of
coords, tiles, and possibly npcs. """
from foxtrot.models.chunk import generator


class Chunk:
    def __init__(self, random, x=None, y=None, width=None, height=None, max_size=10000):
        self.random = random
        self.width = width
        self.height = height
        self.x = (
            random.randint(self.width // 2, max_size - self.width // 2)
            if x is None
            else x
        )
        self.y = (
            random.randint(self.height // 2, max_size - self.height // 2)
            if y is None
            else y
        )
        self.npcs = []
        self.tiles = generator.Generator(self.width, self.height)
        self.tiles.place_random_rooms(8, 16, 2, 1, 100)
        self.tiles.generate_corridors("l")
        self.tiles.prune_deadends(50)
        self.tiles.generate_airlocks()
        self.tiles.connect_all_rooms(0)
        self.tiles.join_unconnected_areas(self.tiles.find_unconnected_areas())
        self.tiles.place_walls()

    def update(self):
        for npc in npcs:
            npc.update()

    def aabb(self, x, y):
        """ return True if x,y coords are inside this chunk """
        return abs(self.x - x) < self.width // 2 and abs(self.y - y) < self.height // 2

    def passable(self, x, y):
        """ return True if the x,y coordinates are possible within chunk """
        try:
            rel_x = int(x) - self.x + self.width // 2
            rel_y = int(y) - self.y + self.height // 2
            tile = self.tiles.grid[rel_x][rel_y]
            return (
                tile == generator.FLOOR
                or tile == generator.CORRIDOR
                or tile == generator.DOOR
            )
        except IndexError as e:
            print("Exception determining chunk passability: %s" % str(e))
            return True
