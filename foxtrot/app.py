import pyxel

from foxtrot.ui.screens.menu import MenuScreen


class App:
    def __init__(self):
        self.screens = [MenuScreen(self)]
        pyxel.constants.APP_MAX_WINDOW_SIZE = 3840
        pyxel.constants.DRAW_MAX_COUNT = 2 ** 16
        pyxel.init(256, 256, caption="foxtrot")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.screens[-1].update()

    def draw(self):
        pyxel.cls(1)
        self.screens[-1].draw()

    def push(self, screen):
        self.screens.append(screen)

    def pop(self):
        self.screens.pop()


App()
