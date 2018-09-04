from abc import ABC


class Mission(ABC):
    def update(self, world):
        if hasattr(self, "trigger"):
            self.trigger.update(world)

    def should_trigger(self, world):
        if hasattr(self, "trigger"):
            return self.trigger.should_trigger(world)
        raise NotImplemented

    def manifest(self, world):
        if hasattr(self, "manifestation"):
            return self.manifestation.manifest(world)
        raise NotImplemented
