from foxtrot import log, math
from foxtrot.models.chunk.chunk import Chunk
from foxtrot.models.chunk.room_type import RoomType

logger = log.create_logger(__name__)


class Colony(Chunk):
    def __init__(self, random, **kwargs):
        size = 64
        while not hasattr(self, 'tiles') or len(self.tiles.rooms) != 1:
            Chunk.__init__(self, random, width=size, height=size, room_tries=2, **kwargs)
        self.tiles.rooms[0].type = RoomType.CONTROL
