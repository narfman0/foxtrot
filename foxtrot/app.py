import pyxel

from foxtrot import saves, settings
from foxtrot.ui.screens.menu import MenuScreen


class App:
    def __init__(self):
        pyxel.constants.APP_MAX_WINDOW_SIZE = 3840
        pyxel.constants.APP_MAX_SCREEN_SIZE = 3840
        pyxel.constants.DRAW_MAX_COUNT = 2 ** 16
        saves.load_settings()
        self.screens = [MenuScreen(self)]
        pyxel.init(
            settings.settings['screen_width'],
            settings.settings['screen_height'],
            caption="foxtrot",
            scale=settings.settings['scale'],
        )
        pyxel.run(self.update, self.draw)

    def update(self):
        self.screens[-1].update()

    def draw(self):
        pyxel.cls(1)
        self.screens[-1].draw()

    def push(self, screen):
        self.screens.append(screen)

    def pop(self):
        self.screens.pop()


App()
