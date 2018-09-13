from foxtrot.models.missions.triggers.trigger import Trigger


class PopulationTrigger(Trigger):
    def __init__(self, count):
        self.count = count

    def should_trigger(self, world):
        return len(world.get_colony().npcs) >= self.count
