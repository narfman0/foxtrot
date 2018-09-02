from foxtrot.models.missions.triggers.trigger import Trigger


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
