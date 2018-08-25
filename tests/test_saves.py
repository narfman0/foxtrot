from unittest import mock, TestCase

from foxtrot.models.world import World
from foxtrot.models import saves


class WorldTest(TestCase):
    @mock.patch("foxtrot.models.world.random.randint")
    def test_save_load(self, randint):
        name = "test1"
        randint.return_value = 1
        world = World(seed=0, size=0)
        world.player.name = name
        saves.save(world)
        world = saves.load(name)
        self.assertEquals(name, world.player.name)
