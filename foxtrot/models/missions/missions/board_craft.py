from foxtrot import log
from foxtrot.models.chunk import RoomType, Ship
from foxtrot.models.missions.missions.mission import Mission
from foxtrot.models.missions import manifestations, triggers

logger = log.create_logger(__name__)


class BoardCraftMission(Mission):
    manifestation = manifestations.LogManifestation("Craft boarded and on bridge")

    def __init__(self, random, world):
        ship = None
        for chunk in world.chunks[::-1]:
            if isinstance(chunk, Ship):
                ship = chunk
                break
        if ship == None:
            logger.warning("Ship not found in world!")
            return
        bridge = None
        for room in ship.tiles.rooms:
            if getattr(room, "type", None) == RoomType.BRIDGE:
                bridge = room
                break
        if bridge == None:
            logger.warning("Bridge not found on ship %s!", ship)
            return
        self.trigger = triggers.RoomTrigger(room)
        # TODO trigger menu instead of log :)
        # self.manifestation = manifestations.MenuManifestation(callback, options)
