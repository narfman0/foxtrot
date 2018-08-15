import pyxel


class Menu:
    def __init__(self, options):
        self.options = options
        self.current_option = 0

    def update(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.options[self.current_option][1]()
        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.current_option == len(self.options) - 1:
                self.current_option = 0
            else:
                self.current_option += 1
        if pyxel.btnp(pyxel.KEY_UP):
            if self.current_option == 0:
                self.current_option = len(self.options) - 1
            else:
                self.current_option -= 1

    def draw(self):
        for index, option in enumerate(self.options):
            text = option[0]
            color = 7 if index == self.current_option else 2
            pyxel.text(
                pyxel.width / 2 - len(text) * 4 / 2,
                pyxel.height / 2 + 8 * index,
                text,
                color,
            )
