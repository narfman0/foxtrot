from foxtrot import log
from foxtrot.models.missions.triggers.trigger import Trigger

logger = log.create_logger(__name__)


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
