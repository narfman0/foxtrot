import pyxel


class MenuScreen:
    def update(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            pyxel.quit()

    def draw(self):
        pyxel.text(pyxel.width / 2, 16, "yo", pyxel.frame_count % 16)
