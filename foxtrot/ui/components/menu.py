import pyxel

from foxtrot import log

logger = log.create_logger(__name__)


class Menu:
    border_width = 4
    text_height = 8

    def __init__(self, options, background_color=None):
        self.options = options
        self.current_option = 0
        self.background_color = background_color
        self.height = len(self.options) * self.text_height + self.border_width
        self.width = (
            max([len(option[0]) for option in self.options]) * 4 + self.border_width
        )
        logger.debug("Created menu with options: %s", options)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            selection = self.options[self.current_option]
            logger.debug("Menu selected option: %s", selection)
            selection[1]()
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
        if self.background_color:
            x1 = pyxel.width // 2 - self.width // 2
            y1 = pyxel.height // 2 - self.height // 2
            pyxel.rect(x1, y1, x1 + self.width, y1 + self.height, self.background_color)
        for index, option in enumerate(self.options):
            text = option[0]
            color = 7 if index == self.current_option else 2
            x = pyxel.width / 2 - len(text) * 2 + self.border_width // 2
            y = (
                pyxel.height / 2
                + self.text_height * index
                - self.height // 2
                + self.border_width // 2
            )
            pyxel.text(x, y, text, color)
