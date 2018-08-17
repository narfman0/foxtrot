import random
from unittest import TestCase

from foxtrot.models.chunk import Chunk


class ChunksTest(TestCase):
    def setUp(self):
        random.seed(0)

    def test_chunk_aabb(self):
        chunk = Chunk(random, x=0, y=0, size=4)
        self.assertTrue(chunk.aabb(0, 0))
        self.assertFalse(chunk.aabb(5, 5))
