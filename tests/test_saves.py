from unittest import mock, TestCase

from foxtrot import saves
from foxtrot.models import NPC, World


class WorldTest(TestCase):
    def test_save_load(self):
        name = "test1"
        world = World()
        player = NPC(name=name)
        world.player = player
        saves.save(world)
        world = saves.load(name)
        self.assertEquals(name, world.player.name)
