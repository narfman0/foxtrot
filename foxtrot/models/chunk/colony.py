from foxtrot import log, math
from foxtrot.models.chunk.chunk import Chunk
from foxtrot.models.chunk.room_type import RoomType

logger = log.create_logger(__name__)
FRAMES_BETWEEN_MINING_CHECKS = 5 * 60


class Colony(Chunk):
    def __init__(self, random, **kwargs):
        size = 64
        while not hasattr(self, "tiles") or len(self.tiles.rooms) != 1:
            Chunk.__init__(
                self, random, width=size, height=size, room_tries=2, **kwargs
            )
        self.tiles.rooms[0].type = RoomType.CONTROL
        self.mining_check_frame = 0

    def add_room(self, room_type):
        current_rooms = len(self.tiles.rooms)
        attemps = 32
        room = None
        self.tiles.remove_walls()
        while room is None and attemps > 0:
            self.tiles.place_random_rooms(
                self.room_min_size // 2, self.room_max_size // 2, 2, 1, 1
            )
            if len(self.tiles.rooms) == current_rooms:
                attemps -= 1
                continue
            self.tiles.connect_all_rooms(0)
            self.tiles.join_unconnected_areas(self.tiles.find_unconnected_areas())
            room = self.tiles.rooms[-1]
            room.type = room_type
        self.tiles.place_walls()
        if room is None:
            logger.warning("Failed to create room: %s", room_type.name)
        return room

    def update(self, world):
        Chunk.update(self, world)
        if self.mining_check_frame <= 0:
            fuel_unused = getattr(self, "fuel_unused", 0.0)
            mining_count, refinery_count = self.get_mining_count()
            mining_affinity, refinery_affinity = self.get_mining_affinity_counts()
            fuel_created = min(
                mining_count * math.productivity(mining_affinity),
                refinery_count * math.productivity(refinery_affinity),
            )
            fuel_unused += fuel_created
            fuel_made = int(fuel_unused)
            self.fuel_unused = fuel_unused - fuel_made
            world.fuel += fuel_made
            self.mining_check_frame = FRAMES_BETWEEN_MINING_CHECKS
        else:
            self.mining_check_frame -= 1

    def get_mining_count(self):
        """ Return the count of mining/refinery pairs """
        mining = 0
        refinery = 0
        for room in self.tiles.rooms:
            room_type = getattr(room, "type", None)
            if room_type == RoomType.MINING:
                mining += 1
            elif room_type == RoomType.REFINERY:
                refinery += 1
        return mining, refinery

    def get_mining_affinity_counts(self):
        """ Return tuple of mining/refinery affinities """
        mining = 0
        refinery = 0
        for npc in self.npcs:
            room_type = getattr(npc, "affinity", None)
            if room_type == RoomType.MINING:
                mining += 1
            elif room_type == RoomType.REFINERY:
                refinery += 1
        return mining, refinery
