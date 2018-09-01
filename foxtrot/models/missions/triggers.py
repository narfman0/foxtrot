from abc import ABC
from foxtrot import log

logger = log.create_logger(__name__)


class Trigger(ABC):
    def should_trigger(self, world):
        """ return True, False if we should trigger or no """
        return NotImplemented

    def update(self, world):
        """ Optional update method called once per frame """
        pass


class BooleanTrigger(Trigger):
    def __init__(self, trigger=True):
        self.trigger = trigger

    def should_trigger(self, world):
        return self.trigger


class FrameTrigger(Trigger):
    def __init__(self, frames):
        self.frames = frames
        self.frame = 0

    def should_trigger(self, world):
        if self.frame >= self.frames:
            logger.info("Should trigger FrameTrigger")
            return True

    def update(self, world):
        self.frame += 1


class RoomTrigger(Trigger):
    def __init__(self, room):
        self.room = room
        self.colliding = False

    def should_trigger(self, world):
        return self.colliding

    def update(self, world):
        found = False
        for chunk in world.chunks:
            if not chunk.aabb(world.player.x, world.player.y):
                continue
            candidate_room = chunk.get_room(world.player.x, world.player.y)
            if candidate_room == self.room:
                self.colliding = True
                found = True
                break
        if not found:
            self.colliding = False
