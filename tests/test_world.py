from unittest import mock, TestCase

from foxtrot.models import World
from foxtrot.models.chunk.ship import TRAVEL_FRAMES


class WorldTest(TestCase):
    world = World().create(seed=0, size=0)

    def test_world(self):
        self.assertTrue(len(self.world.chunks) > 0)

    def test_get_destinations(self):
        destinations = self.world.get_destinations(2, 2)
        self.assertEquals(4, len(destinations))

    @mock.patch("foxtrot.models.world.random.randint")
    def test_world_travel(self, randint):
        randint.return_value = 0
        ship = self.world.chunks[-1]
        dest = self.world.chunks[0]
        self.world.travel(ship, dest)

    def test_ship_travel(self):
        ship = self.world.chunks[-1]
        ship.x = 0
        ship.y = 0
        ship.travel(100, 100)
        self.assertTrue(ship.traveling)
        for _ in range(TRAVEL_FRAMES + 1):
            ship.update(self.world)
        self.assertFalse(ship.traveling)
        self.assertEquals(ship.x, 100)
        self.assertEquals(ship.y, 100)
