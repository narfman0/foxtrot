from foxtrot.models.missions.missions import AwakeMission, DebriefMission


def create_missions(random, world):
    """ Create missions for player """
    # TODO we might want to make this a graph or something... we might want
    # multiples active at once..? sorted at least?
    missions = []
    missions.append(AwakeMission())
    missions.append(DebriefMission(random, world))
    return missions
