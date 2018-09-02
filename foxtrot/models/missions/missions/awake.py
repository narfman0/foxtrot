from foxtrot.models.missions import manifestations, triggers
from foxtrot.models.missions.missions.mission import Mission


class AwakeMission(Mission):
    trigger = triggers.FrameTrigger(3 * 60)
    manifestation = manifestations.LogManifestation("First trigger hit")
