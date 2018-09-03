from foxtrot.models.missions.manifestations.manifestation import Manifestation


class MenuManifestation(Manifestation):
    def __init__(self, callback, text, options):
        self.callback = callback
        self.text = text
        self.options = options

    def manifest(self, world):
        self.callback(self.text, self.options)
