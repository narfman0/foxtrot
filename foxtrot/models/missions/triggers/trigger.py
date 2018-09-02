from abc import ABC


class Trigger(ABC):
    def should_trigger(self, world):
        """ return True, False if we should trigger or no """
        return NotImplemented

    def update(self, world):
        """ Optional update method called once per frame """
        pass
