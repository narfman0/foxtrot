from foxtrot import log
from foxtrot.models.chunk import RoomType
from foxtrot.models.missions.missions.mission import Mission
from foxtrot.models.missions import manifestations, triggers

logger = log.create_logger(__name__)


class DebriefMission(Mission):
    def __init__(self, random, world):
        rooms = world.home_chunk.tiles.rooms
        room = None
        tries = 4 * len(rooms)
        while not room:
            candidate_room = random.choice(rooms)
            if not hasattr(candidate_room, "type"):
                room = candidate_room
                room.type = RoomType.CORPORATION
            if tries <= 0:
                logger.warning(
                    "Ran out of tries for InitialDebriefMission room selection"
                )
                break
            else:
                tries += 1
        self.trigger = triggers.RoomTrigger(room)

    def manifest(self, world):
        text = "Youve cost us much. Last chance - start a colony or else"
        options = ["Affirmative", "Can do, sir"]
        world.create_menu(text, options)
