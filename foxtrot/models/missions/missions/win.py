from foxtrot import log
from foxtrot.models.chunk import RoomType, Colony
from foxtrot.models.missions.missions.mission import Mission
from foxtrot.models.missions import manifestations, triggers

logger = log.create_logger(__name__)
TARGET_POPULATION = 10


class WinMission(Mission):
    trigger = triggers.PopulationTrigger(TARGET_POPULATION)

    def manifest(self, random, world):
        text = "Great job, you've built your colony to %d and win!" % TARGET_POPULATION
        options = ["Affirmative", "Hurrah"]
        world.create_menu(text, options)
