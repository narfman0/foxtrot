from abc import ABC
from foxtrot import log

logger = log.create_logger(__name__)


class Manifestation(ABC):
    def manifest(self, world):
        return NotImplemented


class MenuManifestation(Manifestation):
    def __init__(self, callback, options):
        self.callback = callback
        self.options = options

    def manifest(self, world):
        self.callback(self.options)


class LogManifestation(Manifestation):
    def __init__(self, message):
        self.message = message

    def manifest(self, world):
        logger.warning(self.message)
