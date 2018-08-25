import random
from unittest import TestCase
from unittest.mock import Mock

from foxtrot.models.npc import NPC


class NPCTest(TestCase):
    def setUp(self):
        random.seed(1)
        self.world = Mock()
        self.world.npc_in_chunk.return_value = []

    def test_npc_velocity(self):
        npc = NPC(random=random, x=1, y=2, dx=1, dy=2)
        self.assertEquals(1, npc.x)
        self.assertEquals(2, npc.y)
        npc.update(self.world)
        self.assertEquals(2, npc.x)
        self.assertEquals(4, npc.y)
