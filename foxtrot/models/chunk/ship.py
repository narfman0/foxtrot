from enum import Enum

from foxtrot.models.chunk.chunk import Chunk


class RoomType(Enum):
    BRIDGE = 1
    ENGINEERING = 2
    WEAPONS = 3
    LIFE = 4
    CARGO = 5


class Ship(Chunk):
    SIZES = [(16, 8), (32, 14), (64, 24)]
    MIN_ROOMS = 4

    def __init__(
        self,
        random,
        x=None,
        y=None,
        width=None,
        height=None,
        max_size=10000,
        room_min_size=None,
        room_max_size=None,
    ):
        size = random.choice(self.SIZES)
        width = width if width else size[0]
        height = height if height else size[1]
        room_min_size = room_min_size if room_min_size else 4
        room_max_size = room_max_size if room_max_size else 6
        Chunk.__init__(
            self,
            random,
            x=x,
            y=y,
            width=width,
            height=height,
            max_size=max_size,
            room_min_size=room_min_size,
            room_max_size=room_max_size,
        )
        for room in range(Ship.MIN_ROOMS):
            self.tiles.rooms[room].type = RoomType(1 + room)
