from foxtrot.models.missions import mission


def create_missions(random, world):
    """ Create missions for player """
    # TODO we might want to make this a graph or something... we might want
    # multiples active at once..? sorted at least?
    missions = []
    missions.append(mission.FirstMission())
    return missions
