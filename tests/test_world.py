from unittest import mock, TestCase

from foxtrot.models.world import World


world = World(seed=0, size=0)


class WorldTest(TestCase):
    def test_world(self):
        self.assertTrue(len(world.chunks) > 0)

    def test_get_destinations(self):
        destinations = world.get_destinations(2, 2)
        self.assertEquals(4, len(destinations))

    @mock.patch("foxtrot.models.world.random")
    def test_fly(self, random):
        random.randint.return_value = 0
        ship = world.chunks[-1]
        dest = world.chunks[0]
        world.travel(ship, dest)
        self.assertTrue(ship.x < 800)

    def test_travel(self):
        ship = world.chunks[-1]
        ship.x = 0
        ship.y = 0
        ship.travel(100, 100)
        self.assertTrue(ship.traveling)
        for _ in range(50):
            ship.update()
        self.assertFalse(ship.traveling)
        self.assertEquals(ship.x, 100)
        self.assertEquals(ship.y, 100)
