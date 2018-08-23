from foxtrot import log, math
from foxtrot.models.chunk.chunk import Chunk
from foxtrot.models.chunk.room_type import RoomType

TRAVEL_FRAMES = 60
logger = log.create_logger(__name__)


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
        self.traveling = False
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

    def update(self, world):
        if self.traveling:
            dst_x, dst_y = self.travel_destination
            if self.travel_frame >= TRAVEL_FRAMES:
                self.traveling = False
                self.dx = 0
                self.dy = 0
                self.move(dst_x - self.x, dst_y - self.y)
                self.x = dst_x
                self.y = dst_y
                logger.info("%s completed trip to %s", self, self.travel_destination)
            else:
                self.travel_frame += 1
                percent = float(self.travel_frame / TRAVEL_FRAMES)
                progress = math.smoothstep(percent)
                x, y = math.lerp(self.travel_origin, self.travel_destination, progress)
                self.move(x - self.x, y - self.y)
        Chunk.update(self, world)

    def travel(self, x, y):
        """ Set up travel to the given RELATIVE x,y coordinates """
        self.traveling = True
        self.travel_destination = (self.x + x, self.y + y)
        self.travel_origin = (self.x, self.y)
        self.travel_frame = 0
