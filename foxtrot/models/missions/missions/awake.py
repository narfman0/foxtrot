from foxtrot.models.missions import manifestations, triggers
from foxtrot.models.missions.missions.mission import Mission


class AwakeMission(Mission):
    trigger = triggers.FrameTrigger(7 * 60)

    def __init__(self, random, world):
        text = "Cap! Head to the closest %s office, stat." % world.company_name
        options = [
            ("Affirmative", self.complete),
            ("Time to hit the ol' dusty trail", self.complete),
        ]
        callback = lambda *args: world.create_menu(text, options)
        self.manifestation = manifestations.MenuManifestation(callback, text, options)

    def complete(self):
        pass
