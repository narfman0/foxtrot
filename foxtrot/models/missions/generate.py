from foxtrot.models.missions import missions


def create_missions(random, world):
    """ Create missions for player """
    return [
        missions.AwakeMission(random, world),
        missions.BoardCraftMission(random, world),
        missions.DebriefMission(random, world),
        missions.WinMission(random, world),
    ]
