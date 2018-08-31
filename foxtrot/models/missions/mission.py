from abc import ABC
from foxtrot.models.missions import manifestations, triggers


class Mission(ABC):
    pass


class FirstMission(Mission):
    trigger = triggers.FrameTrigger(3 * 60)
    manifestation = manifestations.LogManifestation("First trigger hit")
