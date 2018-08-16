import pyxel


class GameplayScreen:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager

    def update(self):
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.screen_manager.pop()

    def draw(self):
        pyxel.text(pyxel.width / 2 - 16, 64, "gameplay", pyxel.frame_count % 16)
