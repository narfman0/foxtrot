from foxtrot import log
from foxtrot.models.missions.manifestations.manifestation import Manifestation

logger = log.create_logger(__name__)


class LogManifestation(Manifestation):
    def __init__(self, message):
        self.message = message

    def manifest(self, world):
        logger.info(self.message)
