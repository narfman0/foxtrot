from foxtrot.models.missions.manifestations.manifestation import Manifestation


class MenuManifestation(Manifestation):
    def __init__(self, callback, options):
        self.callback = callback
        self.options = options

    def manifest(self, world):
        self.callback(self.options)
