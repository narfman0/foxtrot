from unittest import TestCase

from foxtrot.models.npc import NPC
from foxtrot.models.world import World


class ModelsTest(TestCase):
    def test_npc_velocity(self):
        npc = NPC(x=1, y=2, dx=1, dy=2)
        self.assertEquals(1, npc.x)
        self.assertEquals(2, npc.y)
        npc.update()
        self.assertEquals(2, npc.x)
        self.assertEquals(4, npc.y)

    def test_world(self):
        world = World(seed=0, size=0)
        self.assertTrue(len(world.chunks) > 0)
