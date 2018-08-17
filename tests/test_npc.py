from unittest import TestCase

from foxtrot.models.npc import NPC


class NPCTest(TestCase):
    def test_npc_velocity(self):
        npc = NPC(x=1, y=2, dx=1, dy=2)
        self.assertEquals(1, npc.x)
        self.assertEquals(2, npc.y)
        npc.update()
        self.assertEquals(2, npc.x)
        self.assertEquals(4, npc.y)
