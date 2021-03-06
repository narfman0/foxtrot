""" A chunk is a meaningful part of the world. It includes bounding box of
coords, tiles, and possibly npcs. """
from foxtrot import log
from foxtrot.models.chunk import generator
from foxtrot.models.chunk.room_type import RoomType
from foxtrot.models import words


logger = log.create_logger(__name__)


class Chunk:
    def __init__(
        self,
        random,
        x=None,
        y=None,
        dx=None,
        dy=None,
        width=None,
        height=None,
        max_size=10000,
        room_min_size=8,
        room_max_size=16,
        room_tries=200,
        name=None,
        create=True,
    ):
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
        self.dx = dx if dx is not None else 0
        self.dy = dy if dy is not None else 0
        self.name = name if name else words.generate(random)
        self.npcs = set()
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.room_tries = room_tries
        self.tileset = random.randint(0, 7)
        if create:
            self.create()

    def create(self):
        self.tiles = generator.Generator(width=self.width, height=self.height)
        self.tiles.place_random_rooms(
            self.room_min_size, self.room_max_size, 2, 1, self.room_tries
        )
        self.tiles.generate_corridors("f")
        self.tiles.prune_deadends(50)
        self.tiles.generate_airlocks()
        self.tiles.connect_all_rooms(0)
        self.tiles.join_unconnected_areas(self.tiles.find_unconnected_areas())
        self.tiles.place_walls()

    def initialize_traders(self, random, frequency=8):
        """ Rough frequency of rooms. 8 would be about 1/8 of rooms are TRADER """
        total = 0
        target = len(self.tiles.rooms) // frequency
        for room in self.tiles.rooms:
            if total >= target:
                return
            if getattr(room, "type", None) is None:
                room.type = RoomType.TRADER
                room.salvage_cost = random.randint(90, 110)
                room.fuel_cost = random.randint(55, 75)
                total += 1

    def initialize_crew(self, random, frequency=10):
        """ Rough frequency of rooms """
        total = 0
        target = len(self.tiles.rooms) // frequency
        for room in self.tiles.rooms:
            if total >= target:
                return
            if getattr(room, "type", None) is None:
                room.type = RoomType.CREW
                room.cost = random.randint(3400, 6400)
                total += 1

    def update(self, world):
        self.x += self.dx
        self.y += self.dy

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
            logger.warning("Exception determining chunk passability: %s", e)
            return True

    def get_room(self, x, y):
        """ return room if x,y coordinates lie within a room """
        rel_x = int(x) - self.x + self.width // 2
        rel_y = int(y) - self.y + self.height // 2
        for room in self.tiles.rooms:
            if (
                rel_x >= room.x
                and rel_x < room.x + room.width
                and rel_y >= room.y
                and rel_y < room.y + room.height
            ):
                return room
        return None

    def get_rooms_with_type(self, room_type):
        for room in self.tiles.rooms:
            if getattr(room, "type", None) == room_type:
                yield room

    def get_room_position(self, room):
        x = self.x - self.width // 2 + room.x + room.width // 2
        y = self.y - self.height // 2 + room.y + room.height // 2
        return x, y

    def move(self, x, y):
        """ Directly move by the given x,y """
        self.x += x
        self.y += y
        for npc in self.npcs:
            npc.move(x, y)

    @property
    def airlock_x(self):
        """ Return airlocks x coord relative to its center """
        return self.tiles.airlock_x - self.width // 2

    @property
    def airlock_y(self):
        """ Return airlocks y coord relative to its center """
        return self.tiles.airlock_y - self.height // 2

    @property
    def position(self):
        return self.x, self.y

    def __repr__(self):
        return self.name + " x,y: %d,%d" % self.position
