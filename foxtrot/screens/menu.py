import pyxel

from foxtrot.components.menu import Menu


class MenuScreen:
    def __init__(self):
        def quit():
            pyxel.quit()

        self.menu = Menu([("Start Game", self.start_game), ("Quit", quit)])

    def update(self):
        self.menu.update()

    def draw(self):
        self.menu.draw()
        pyxel.text(pyxel.width / 2, 64, "yo", pyxel.frame_count % 16)

    def start_game(self):
        # TODO start the game :)
        raise NotImplementedError("start_game not implemented")
