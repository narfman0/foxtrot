from foxtrot import log, math
from foxtrot.models.chunk.chunk import Chunk
from foxtrot.models.chunk.room_type import RoomType

logger = log.create_logger(__name__)
FRAMES_BETWEEN_MINING_CHECKS = 5 * 60


class Colony(Chunk):
    def __init__(self, random, **kwargs):
        size = 64
        while not hasattr(self, 'tiles') or len(self.tiles.rooms) != 1:
            Chunk.__init__(self, random, width=size, height=size, room_tries=2, **kwargs)
        self.tiles.rooms[0].type = RoomType.CONTROL
        self.mining_check_frame = 0

    def add_room(self, room_type):
        current_rooms = len(self.tiles.rooms)
        attemps = 32
        room = None
        self.tiles.remove_walls()
        while room is None and attemps > 0:
            self.tiles.place_random_rooms(self.room_min_size // 2, self.room_max_size // 2, 2, 1, 1)
            if len(self.tiles.rooms) == current_rooms:
                attemps -= 1
                continue
            self.tiles.connect_all_rooms(0)
            self.tiles.join_unconnected_areas(self.tiles.find_unconnected_areas())
            room = self.tiles.rooms[-1]
            room.type = room_type
        self.tiles.place_walls()
        if room is None:
            logger.warning('Failed to create room: %s', room_type.name)
        return room

    def update(self, world):
        Chunk.update(self, world)
        if self.mining_check_frame <= 0:
            world.fuel += self.get_mining_count()
            self.mining_check_frame = FRAMES_BETWEEN_MINING_CHECKS
        else:
            self.mining_check_frame -= 1

    def get_mining_count(self):
        """ Return the count of mining/refinery pairs """
        mining = 0
        refinery = 0
        for room in self.tiles.rooms:
            room_type = getattr(room, 'type', None)
            if room_type == RoomType.MINING:
                mining += 1
            elif room_type == RoomType.REFINERY:
                refinery += 1
        return min(mining, refinery)
