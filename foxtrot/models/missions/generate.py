from foxtrot.models.missions import missions


def create_missions(random, world):
    """ Create missions for player """
    # TODO we might want to make this a graph or something... we might want
    # multiples active at once..? sorted at least?
    return [
        missions.AwakeMission(),
        missions.BoardCraftMission(random, world),
        missions.DebriefMission(random, world),
    ]
