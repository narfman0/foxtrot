from unittest import TestCase

from foxtrot.models.world import World


world = World(seed=0, size=0)


class WorldTest(TestCase):
    def test_world(self):
        self.assertTrue(len(world.chunks) > 0)

    def test_get_destinations(self):
        destinations = world.get_destinations(2, 2)
        self.assertEquals(4, len(destinations))
