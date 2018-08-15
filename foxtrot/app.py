import pyxel

from foxtrot.screens.menu import MenuScreen


class App:
    def __init__(self):
        self.screens = [MenuScreen()]
        pyxel.init(256, 192, caption="foxtrot")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.screens[-1].update()

    def draw(self):
        pyxel.cls(1)
        self.screens[-1].draw()


App()
