from unittest import TestCase

from foxtrot.models.world import World


class WorldTest(TestCase):
    def test_world(self):
        world = World(seed=0, size=0)
        self.assertTrue(len(world.chunks) > 0)
