from foxtrot.models.missions.triggers.trigger import Trigger


class BooleanTrigger(Trigger):
    def __init__(self, trigger=True):
        self.trigger = trigger

    def should_trigger(self, world):
        return self.trigger
