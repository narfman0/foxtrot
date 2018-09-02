from abc import ABC


class Manifestation(ABC):
    def manifest(self, world):
        return NotImplemented
