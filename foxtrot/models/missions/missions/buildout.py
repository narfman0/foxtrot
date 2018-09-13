from foxtrot import log
from foxtrot.models.chunk import RoomType, Colony
from foxtrot.models.missions.missions.mission import Mission
from foxtrot.models.missions import manifestations, triggers

logger = log.create_logger(__name__)


class BuildoutMission(Mission):
    def __init__(self, random, world):
        colony = world.get_colony()
        if colony == None:
            logger.warning("Colony not found in world!")
            return
        control = None
        for room in colony.tiles.rooms:
            if getattr(room, "type", None) == RoomType.CONTROL:
                control = room
                break
        if control == None:
            logger.warning("Control not found on colony %s!", ship)
            return
        self.trigger = triggers.RoomTrigger(room)
        self.colony_name = colony.name

    def manifest(self, random, world):
        text = "Welcome to %s! It is time to start the buildout." % self.colony_name
        options = ["Affirmative", "On it, boss man"]
        world.create_menu(text, options)
