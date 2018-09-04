from foxtrot import log, math
from foxtrot.models.chunk.chunk import Chunk
from foxtrot.models.chunk.room_type import RoomType

logger = log.create_logger(__name__)


class Colony(Chunk):
    def __init__(self, random, **kwargs):
        width = 64
        height = 64
        Chunk.__init__(self, random, width=width, height=height, **kwargs)
        self.tiles.rooms[0].type = RoomType.CONTROL
