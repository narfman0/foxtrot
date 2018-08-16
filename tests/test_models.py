from unittest import TestCase

from foxtrot.models.npc import NPC
from foxtrot.models.world import World


class ModelsTest(TestCase):
    def test_npc_velocity(self):
        npc = NPC(1, 2, 1, 2)
        self.assertEquals(1, npc.x)
        self.assertEquals(2, npc.y)
        npc.update()
        self.assertEquals(2, npc.x)
        self.assertEquals(4, npc.y)
