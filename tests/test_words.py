import random
from unittest import TestCase

from foxtrot.models import words


class NPCTest(TestCase):
    def setUp(self):
        random.seed(0)

    def test_generate(self):
        word = words.generate(random)
        self.assertTrue(len(word) > 5)
