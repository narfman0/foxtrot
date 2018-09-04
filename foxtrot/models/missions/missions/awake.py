from foxtrot.models.missions import manifestations, triggers
from foxtrot.models.missions.missions.mission import Mission


class AwakeMission(Mission):
    trigger = triggers.FrameTrigger(3 * 60)

    def __init__(self, random, world):
        pass

    def manifest(self, random, world):
        text = "Cap! You ok? Head to your ship - should be nearby."
        options = ["Affirmative", "Time to hit the ol' dusty trail"]
        world.create_menu(text, options)
